"""
ReviewGuard AI — Agent 9: Finalization Agent
Completes the pipeline: updates review_cycle to COMPLETED, emits final audit event.
Only runs after APPROVE action. SLO: < 1 second.
"""

from datetime import datetime, timezone

import structlog

from app.ai.state.review_state import ReviewGuardState
from core.database import SessionLocal
from models.enums import ReviewCycleStatus, AuditEventType
from repositories import audit_repo
from sqlalchemy import text

logger = structlog.get_logger(__name__)


def finalization_node(state: ReviewGuardState) -> dict:
    """
    Finalization Agent Node.
    - Sets review_cycle.status = COMPLETED
    - Emits PIPELINE_COMPLETED audit event with full cost/token summary
    - Sets pipeline_status = COMPLETED
    """
    agent_name = "finalization_agent"
    start_time = datetime.now(timezone.utc)
    logger.info("agent_started", agent=agent_name, correlation_id=state["correlation_id"])

    db = SessionLocal()
    try:
        # Update review cycle status to COMPLETED
        db.execute(
            text(
                "UPDATE review_cycles SET status = 'COMPLETED', updated_at = now() "
                "WHERE id = :cycle_id"
            ),
            {"cycle_id": state["review_cycle_id"]},
        )

        # Final audit event with full pipeline metrics
        total_tokens = state.get("pipeline_total_tokens", 0)
        total_cost = state.get("pipeline_total_cost_usd", 0.0)
        agents_run = len(state.get("agent_executions", []))

        audit_repo.create(db, {
            "event_type": AuditEventType.PIPELINE_COMPLETED,
            "actor_id": state.get("approval_actor_id"),
            "resource_type": "review_cycle",
            "resource_id": state["review_cycle_id"],
            "event_payload": {
                "pipeline_run_id": state["pipeline_run_id"],
                "report_id": state.get("report_db_id"),
                "total_agents": agents_run,
                "total_tokens": total_tokens,
                "total_cost_usd": total_cost,
                "confidence": state["confidence_result"]["score"] if state.get("confidence_result") else None,
                "claims_count": len(state.get("performance_claims", [])),
                "bias_flags_count": len(state.get("bias_flags", [])),
            },
            "correlation_id": state["pipeline_run_id"],
            "state_version": state["state_version"] + 1,
        })
        db.commit()

        end_time = datetime.now(timezone.utc)
        record = _build_record(
            agent_name, start_time, end_time, "SUCCESS",
            f"Pipeline COMPLETED. Cycle set to COMPLETED. "
            f"Total: {total_tokens} tokens, ${total_cost:.4f} cost.",
        )

        logger.info(
            "pipeline_completed",
            cycle_id=state["review_cycle_id"],
            tokens=total_tokens,
            cost=total_cost,
            correlation_id=state["correlation_id"],
        )

        return {
            "pipeline_status": "COMPLETED",
            "completed_at": end_time.isoformat(),
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
