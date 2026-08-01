"""
ReviewGuard AI — Agent 8: Human Approval Agent (LangGraph Interrupt Node)
Transitions report to PENDING_APPROVAL and interrupts pipeline execution.
Resumes when manager triggers the approval API endpoint.
P3: Human Owns Decisions.
"""

from datetime import datetime, timezone

import structlog

from agents.state import ReviewGuardState
from core.database import SessionLocal
from models.enums import ReportStatus, AuditEventType
from repositories import report_repo, audit_repo
from sqlalchemy import text

logger = structlog.get_logger(__name__)


def human_approval_node(state: ReviewGuardState) -> dict:
    """
    Human Approval Agent Node — LangGraph interrupt point.
    On ENTRY: Transitions report to PENDING_APPROVAL, interrupts execution.
    On RESUME: Reads approval_status written by pipeline_service.resume_pipeline().
    """
    agent_name = "human_approval_agent"
    start_time = datetime.now(timezone.utc)
    logger.info("agent_started", agent=agent_name, correlation_id=state["correlation_id"])

    # If approval_status is already set by resume — we're in the RESUME path
    approval_status = state.get("approval_status", "PENDING")
    if approval_status != "PENDING":
        # Resume path — just pass through; routing handles the branch
        end_time = datetime.now(timezone.utc)
        record = _build_record(
            agent_name, start_time, end_time, "SUCCESS",
            f"Approval action received: {approval_status}.",
        )
        return {
            "state_version": state["state_version"] + 1,
            "current_agent": agent_name,
            "agent_executions": [record],
        }

    # Entry path — transition report to PENDING_APPROVAL
    db = SessionLocal()
    try:
        report_id = state.get("report_db_id")
        if report_id:
            db.execute(
                text("UPDATE reports SET status = 'PENDING_APPROVAL', updated_at = now() WHERE id = :id"),
                {"id": report_id},
            )
            audit_repo.create(db, {
                "event_type": AuditEventType.REPORT_GENERATED,
                "actor_id": None,
                "resource_type": "report",
                "resource_id": report_id,
                "event_payload": {
                    "action": "PENDING_APPROVAL",
                    "manager_id": state["manager_id"],
                    "pipeline_run_id": state["pipeline_run_id"],
                },
                "correlation_id": state["pipeline_run_id"],
                "state_version": state["state_version"] + 1,
            })
            db.commit()

        end_time = datetime.now(timezone.utc)
        record = _build_record(
            agent_name, start_time, end_time, "SUCCESS",
            "Report transitioned to PENDING_APPROVAL. Awaiting manager action.",
        )

        logger.info("pipeline_awaiting_human", report_id=report_id,
                    manager_id=state["manager_id"], correlation_id=state["correlation_id"])

        return {
            "approval_status": "PENDING",
            "approval_required": True,
            "pipeline_status": "AWAITING_HUMAN",
            "state_version": state["state_version"] + 1,
            "current_agent": agent_name,
            "agent_executions": [record],
        }

    except Exception as exc:
        db.rollback()
        logger.exception("agent_failed", agent=agent_name, error=str(exc))
        end_time = datetime.now(timezone.utc)
        record = _build_record(agent_name, start_time, end_time, "FAILURE", str(exc), error_message=str(exc))
        return {
            "pipeline_status": "FAILED",
            "error_state": {"agent": agent_name, "error": str(exc), "timestamp": end_time.isoformat()},
            "state_version": state["state_version"] + 1,
            "agent_executions": [record],
        }
    finally:
        db.close()


def _build_record(agent_name, start, end, status, summary, error_message=None):
    return {
        "agent_name": agent_name,
        "start_time": start.isoformat(),
        "end_time": end.isoformat(),
        "status": status,
        "output_summary": summary,
        "error_message": error_message,
        "items_processed": 0,
        "llm_model_used": None,
        "tokens_prompt": None, "tokens_completion": None, "tokens_total": None,
        "estimated_cost_usd": None,
        "latency_ms": int((end - start).total_seconds() * 1000),
        "prompt_name": None, "prompt_version": None,
        "correlation_id": None, "llm_request_id": None,
    }
