"""
FairTrace — Pipeline Service and Report Approval Service
Pipeline executes as a FastAPI BackgroundTask.
State stored in-memory (dict keyed by pipeline_run_id) for hackathon demo.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional

import structlog

from app.ai.bootstrap.graph_factory import pipeline_graph
from app.ai.state.review_state import ReviewGuardState
from core.database import SessionLocal
from core.exceptions import (
    BusinessValidationError,
    ConflictError,
    ForbiddenError,
    InvalidStateError,
    NotFoundError,
)
from dependencies import CurrentUser
from models.enums import (
    ApprovalAction,
    AuditEventType,
    ReportStatus,
    ReviewCycleStatus,
    UserRole,
)
from repositories import (
    audit_repo,
    report_repo,
    review_cycle_repo,
    review_input_repo,
)
from sqlalchemy import text
from models.db.workflow import WorkflowExecution, WorkflowStatus

logger = structlog.get_logger(__name__)

# ── In-Memory Pipeline State Store ─────────────────────────────────────────────
# Key: pipeline_run_id, Value: ReviewGuardState
_pipeline_store: dict[str, ReviewGuardState] = {}


def get_pipeline_state(pipeline_run_id: str) -> Optional[ReviewGuardState]:
    return _pipeline_store.get(pipeline_run_id)


# ── Pipeline Trigger ───────────────────────────────────────────────────────────

def initialize_pipeline(
    db, cycle_id: str, actor: CurrentUser
) -> str:
    """
    Validates conditions and returns a pipeline_run_id.
    The actual pipeline execution is deferred to a BackgroundTask.
    """
    from uuid import UUID
    cycle = review_cycle_repo.get_by_id(db, UUID(str(cycle_id)))
    if not cycle:
        raise NotFoundError(f"Review cycle {cycle_id} not found.")
    if cycle.status not in (ReviewCycleStatus.ACTIVE, ReviewCycleStatus.PROCESSING):
        raise InvalidStateError("Pipeline can only be triggered for ACTIVE or PROCESSING review cycles.")
    # DB-level stale check
    from sqlalchemy.exc import IntegrityError
    from datetime import datetime, timezone, timedelta
    
    active_workflow = db.query(WorkflowExecution).filter(
        WorkflowExecution.review_id == str(review.id),
        WorkflowExecution.status == WorkflowStatus.RUNNING
    ).first()
    
    if active_workflow:
        # Check heartbeat
        now = datetime.now(timezone.utc)
        if active_workflow.last_heartbeat_at and now - active_workflow.last_heartbeat_at.replace(tzinfo=timezone.utc) > timedelta(minutes=5):
            # It's stale! Mark as FAILED (or RECOVERABLE) so we can retry.
            logger.warning("stale_pipeline_recovered", pipeline_run_id=active_workflow.execution_id)
            active_workflow.status = WorkflowStatus.FAILED
            db.commit()
        else:
            raise ConflictError("A pipeline is already running for this review cycle.")
    input_count = review_input_repo.count_for_cycle(db, UUID(str(cycle_id)))
    if input_count == 0:
        raise BusinessValidationError("At least one input must be submitted before triggering the pipeline.")

    pipeline_run_id = str(uuid.uuid4())

    # Build initial state
    initial_state: ReviewGuardState = {
        "pipeline_run_id": pipeline_run_id,
        "state_version": 0,
        "review_id": str(review.id),
        "employee_id": str(cycle.employee_id),
        "manager_id": str(cycle.manager_id),
        "triggered_by_id": str(actor.id),
        "correlation_id": pipeline_run_id,
        "raw_input_ids": [],
        "validated_inputs": [],
        "intake_complete": False,
        "intake_warnings": [],
        "qdrant_collection_name": "reviewguard_documents",
        "embedded_input_ids": [],
        "total_chunks_created": 0,
        "embedding_complete": False,
        "evidence_index": [],
        "evidence_by_dimension": {},
        "evidence_ready": False,
        "low_evidence_dimensions": [],
        "bias_flags": [],
        "stakeholder_distribution": None,
        "high_bias_count": 0,
        "medium_bias_count": 0,
        "bias_detection_complete": False,
        "dimension_summaries": {},
        "analysis_complete": False,
        "confidence_result": None,
        "performance_claims": [],
        "evidence_citations": [],
        "executive_summary": None,
        "recommended_actions": [],
        "report_db_id": None,
        "report_version": 1,
        "report_complete": False,
        "explanation_traces": [],
        "evaluation_metrics": {},
        "explainability_complete": False,
        "approval_required": False,
        "approval_status": "PENDING",
        "approval_actor_id": None,
        "approval_reason": None,
        "approval_timestamp": None,
        "approval_idempotency_key": None,
        "agent_executions": [],
        "pipeline_total_tokens": 0,
        "pipeline_total_cost_usd": 0.0,
        "pipeline_status": "RUNNING",
        "current_agent": "intake_agent",
        "error_state": None,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "completed_at": None,
    }

    _pipeline_store[pipeline_run_id] = initial_state

    # Trigger PIPELINE_TRIGGERED audit event
    audit_repo.create(db, {
        "event_type": AuditEventType.PIPELINE_TRIGGERED,
        "actor_id": actor.id,
        "actor_role": actor.role,
        "resource_type": "review_cycle",
        "resource_id": cycle.id,
        "event_payload": {"pipeline_run_id": pipeline_run_id, "input_count": input_count},
        "correlation_id": pipeline_run_id,
    })

    # Update cycle status to PROCESSING
    review_cycle_repo.update_status(db, cycle, ReviewCycleStatus.PROCESSING)
    # Create WorkflowExecution in DB
    workflow = WorkflowExecution(
        id=str(uuid.uuid4()),
        execution_id=pipeline_run_id,
        owner_id=actor.id,
        organization_id=str(cycle.organization_id) if hasattr(cycle, 'organization_id') and cycle.organization_id else None,
        review_id=review.id,
        status=WorkflowStatus.RUNNING,
        metadata_=initial_state
    )
    db.add(workflow)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ConflictError("A pipeline is concurrently starting for this review cycle.")

    return pipeline_run_id


def execute_pipeline(pipeline_run_id: str, review_id: str) -> None:
    """
    Executes the LangGraph pipeline.
    Called as FastAPI BackgroundTask — has its own DB session.
    Updates _pipeline_store throughout execution.
    """
    logger.info("pipeline_execution_start", pipeline_run_id=pipeline_run_id)

    state = _pipeline_store.get(pipeline_run_id)
    if not state:
        logger.error("pipeline_state_not_found", pipeline_run_id=pipeline_run_id)
        return

    try:
        final_state = pipeline_graph.invoke(state)
        _pipeline_store[pipeline_run_id] = final_state

        final_status = final_state.get("pipeline_status", "COMPLETED")
        logger.info("pipeline_execution_done",
                    pipeline_run_id=pipeline_run_id, status=final_status)

        # Update WorkflowExecution in DB
        db = SessionLocal()
        try:
            workflow = db.query(WorkflowExecution).filter(WorkflowExecution.execution_id == pipeline_run_id).first()
            if workflow:
                workflow.status = WorkflowStatus.COMPLETED if final_status == "COMPLETED" else WorkflowStatus.FAILED
                workflow.completed_at = datetime.now(timezone.utc)
                db.commit()
        finally:
            db.close()

        # If FAILED, emit failure audit event
        if final_status == "FAILED":
            _emit_failure_audit(pipeline_run_id, review_id, final_state)

    except Exception as exc:
        logger.exception("pipeline_execution_error", pipeline_run_id=pipeline_run_id, error=str(exc))
        if pipeline_run_id in _pipeline_store:
            _pipeline_store[pipeline_run_id]["pipeline_status"] = "FAILED"
            _pipeline_store[pipeline_run_id]["error_state"] = {
                "agent": "orchestrator",
                "error": str(exc),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            
        # Update WorkflowExecution in DB
        db = SessionLocal()
        try:
            workflow = db.query(WorkflowExecution).filter(WorkflowExecution.execution_id == pipeline_run_id).first()
            if workflow:
                workflow.status = WorkflowStatus.FAILED
                workflow.error_state = str(exc)
                db.commit()
        finally:
            db.close()


def _emit_failure_audit(pipeline_run_id: str, review_id: str, state: dict) -> None:
    db = SessionLocal()
    try:
        from uuid import UUID
        audit_repo.create(db, {
            "event_type": AuditEventType.PIPELINE_FAILED,
            "actor_id": None,
            "resource_type": "review_cycle",
            "resource_id": UUID(review_id),
            "event_payload": {
                "pipeline_run_id": pipeline_run_id,
                "error_state": state.get("error_state"),
            },
            "correlation_id": pipeline_run_id,
        })
        db.commit()
    except Exception:
        pass
    finally:
        db.close()


def get_pipeline_status_response(pipeline_run_id: str) -> dict:
    """Returns a pipeline status dict suitable for API response serialization."""
    state = _pipeline_store.get(pipeline_run_id)
    if not state:
        raise NotFoundError(f"Pipeline run {pipeline_run_id} not found.")

    return {
        "pipeline_run_id": pipeline_run_id,
        "review_id": state.get("review_id", ""),
        "pipeline_status": state["pipeline_status"],
        "current_agent": state["current_agent"],
        "agent_executions": state["agent_executions"],
        "pipeline_total_tokens": state.get("pipeline_total_tokens"),
        "pipeline_total_cost_usd": state.get("pipeline_total_cost_usd"),
        "created_at": state["created_at"],
        "completed_at": state.get("completed_at"),
        "error_state": state.get("error_state"),
    }


# ── Report Approval Service ────────────────────────────────────────────────────

# Simple in-memory idempotency store {key: result_dict}
_idempotency_store: dict[str, dict] = {}


def process_approval_action(
    db,
    report_id: str,
    action: ApprovalAction,
    reason: str,
    actor: CurrentUser,
    idempotency_key: str,
    background_tasks = None,
) -> dict:
    """
    Processes APPROVE, REVISION_REQUESTED, or REJECT actions.
    Business rules enforcement per Part 4 Section 8.2.
    """
    from uuid import UUID

    # 1. Idempotency check
    if idempotency_key in _idempotency_store:
        logger.info("idempotent_request_returned", key=idempotency_key)
        return _idempotency_store[idempotency_key]

    # 2. Fetch report
    report = report_repo.get_with_full_details(db, UUID(report_id))
    if not report:
        raise NotFoundError(f"Report {report_id} not found.")

    # 3. Ownership check
    cycle = report.review_cycle
    if actor.role == UserRole.MANAGER and cycle.manager_id != actor.id:
        raise ForbiddenError("You can only approve reports for your own review cycles.")

    # 4. Status guard
    if report.status != ReportStatus.PENDING_APPROVAL:
        raise InvalidStateError(
            f"Report is in status '{report.status.value}'. Only PENDING_APPROVAL reports can be actioned."
        )

    # 5. Reason required
    if not reason or len(reason.strip()) < 10:
        raise BusinessValidationError("Approval reason must be at least 10 characters.")

    # 6. Process action
    now = datetime.now(timezone.utc)
    pipeline_run_id = report.pipeline_run_id

    if action == ApprovalAction.APPROVE:
        db.execute(
            text(
                "UPDATE reports SET status = 'FINALIZED', approved_by = :approved_by, "
                "approved_at = :approved_at, approval_reason = :reason, "
                "approval_idempotency_key = :key, updated_at = now() WHERE id = :id"
            ),
            {
                "approved_by": str(actor.id),
                "approved_at": now,
                "reason": reason,
                "key": idempotency_key,
                "id": report_id,
            },
        )
        # Update review cycle to COMPLETED
        db.execute(
            text("UPDATE review_cycles SET status = 'COMPLETED', updated_at = now() WHERE id = :cycle_id"),
            {"cycle_id": cycle.id},
        )
        event_type = AuditEventType.REPORT_APPROVED

        # Resume pipeline → finalization
        if pipeline_run_id in _pipeline_store:
            _pipeline_store[pipeline_run_id]["approval_status"] = "APPROVED"
            _pipeline_store[pipeline_run_id]["approval_actor_id"] = str(actor.id)
            _pipeline_store[pipeline_run_id]["approval_reason"] = reason
            _pipeline_store[pipeline_run_id]["approval_timestamp"] = now.isoformat()
            _pipeline_store[pipeline_run_id]["approval_idempotency_key"] = idempotency_key

    elif action == ApprovalAction.REVISION_REQUESTED:
        db.execute(
            text(
                "UPDATE reports SET status = 'REVISION_REQUESTED', updated_at = now() WHERE id = :id"
            ),
            {"id": report_id},
        )
        # Update review cycle status
        db.execute(
            text(
                "UPDATE review_cycles SET status = 'PROCESSING', updated_at = now() WHERE id = :cycle_id"
            ),
            {"cycle_id": cycle.id},
        )
        event_type = AuditEventType.REPORT_REVISION_REQUESTED
        db.commit() # ensure report status is saved before triggering pipeline

        if pipeline_run_id in _pipeline_store:
            _pipeline_store[pipeline_run_id]["approval_status"] = "REVISION_REQUESTED"
            _pipeline_store[pipeline_run_id]["approval_reason"] = reason

        # Trigger AI Regeneration
        if background_tasks:
            try:
                new_pipeline_run_id = initialize_pipeline(db, str(cycle.id), actor)
                background_tasks.add_task(execute_pipeline, new_pipeline_run_id, cycle.id)
            except Exception as e:
                logger.error("pipeline_regeneration_failed", error=str(e))

    else:  # REJECT
        db.execute(
            text("UPDATE reports SET status = 'REJECTED', updated_at = now() WHERE id = :id"),
            {"id": report_id},
        )
        event_type = AuditEventType.REPORT_REJECTED

        if pipeline_run_id in _pipeline_store:
            _pipeline_store[pipeline_run_id]["approval_status"] = "REJECTED"
            _pipeline_store[pipeline_run_id]["pipeline_status"] = "COMPLETED"

    audit_repo.create(db, {
        "event_type": event_type,
        "actor_id": actor.id,
        "actor_role": actor.role,
        "resource_type": "report",
        "resource_id": UUID(report_id),
        "event_payload": {
            "action": action.value,
            "reason": reason,
            "idempotency_key": idempotency_key,
        },
        "correlation_id": pipeline_run_id,
    })
    db.commit()

    result = {
        "report_id": report_id,
        "action": action.value,
        "new_status": report.status.value if action != ApprovalAction.APPROVE else "FINALIZED",
        "actioned_by": str(actor.id),
        "actioned_at": now.isoformat(),
        "reason": reason,
    }
    _idempotency_store[idempotency_key] = result
    return result
