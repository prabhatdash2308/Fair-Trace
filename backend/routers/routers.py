"""ReviewGuard AI — Users, ReviewCycles, Inputs, Pipeline, Reports, Audit Routers"""

from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, Query, Request
from sqlalchemy.orm import Session

from dependencies import (
    CurrentUser,
    get_current_user,
    get_db,
    require_admin,
    require_any_authenticated,
    require_manager_or_admin,
)
from models.enums import ReviewCycleStatus, UserRole
from models.schemas import (
    ApprovalActionRequest,
    AuditEventResponse,
    InputResponse,
    InputSubmit,
    PaginatedReviewCycles,
    PipelineTriggerResponse,
    PipelineStatusResponse,
    ReportResponse,
    ReportVersionSummary,
    ReviewCycleCreate,
    ReviewCycleResponse,
    ReviewCycleStatusUpdate,
    UserCreate,
    UserResponse,
)
from core.exceptions import ForbiddenError, NotFoundError
from repositories import report_repo, audit_repo
from services import domain_services, pipeline_service
from models.enums import ApprovalAction


# ── Users Router ───────────────────────────────────────────────────────────────

users_router = APIRouter()


@users_router.post("", response_model=UserResponse, status_code=201,
                   summary="Create User", tags=["Users"])
def create_user(
    body: UserCreate,
    db: Session = Depends(get_db),
    actor: CurrentUser = Depends(require_admin),
):
    return domain_services.create_user(db, body, actor)


@users_router.get("", summary="List Users", tags=["Users"])
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    actor: CurrentUser = Depends(require_admin),
):
    items, total = domain_services.list_users(db, skip, limit)
    return {
        "items": [UserResponse.model_validate(u) for u in items],
        "total": total,
        "skip": skip,
        "limit": limit,
        "has_more": skip + limit < total,
    }


@users_router.get("/{user_id}", response_model=UserResponse, summary="Get User", tags=["Users"])
def get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    actor: CurrentUser = Depends(get_current_user),
):
    if actor.role != UserRole.ADMIN and actor.id != user_id:
        raise ForbiddenError("You can only view your own profile.")
    return domain_services.get_user(db, user_id)


# ── Review Cycles Router ───────────────────────────────────────────────────────

cycles_router = APIRouter()


@cycles_router.post("", response_model=ReviewCycleResponse, status_code=201,
                    summary="Create Review Cycle", tags=["Review Cycles"])
def create_cycle(
    body: ReviewCycleCreate,
    db: Session = Depends(get_db),
    actor: CurrentUser = Depends(require_manager_or_admin),
):
    return domain_services.create_review_cycle(db, body, actor)


@cycles_router.get("", summary="List Review Cycles", tags=["Review Cycles"])
def list_cycles(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    actor: CurrentUser = Depends(require_any_authenticated),
):
    items, total = domain_services.list_review_cycles(db, actor, skip, limit)
    return PaginatedReviewCycles(
        items=[ReviewCycleResponse.model_validate(c) for c in items],
        total=total,
        skip=skip,
        limit=limit,
        has_more=skip + limit < total,
    )


@cycles_router.get("/{cycle_id}", response_model=ReviewCycleResponse,
                   summary="Get Review Cycle", tags=["Review Cycles"])
def get_cycle(
    cycle_id: UUID,
    db: Session = Depends(get_db),
    actor: CurrentUser = Depends(require_any_authenticated),
):
    return domain_services.get_review_cycle(db, cycle_id, actor)


@cycles_router.patch("/{cycle_id}/status", response_model=ReviewCycleResponse,
                     summary="Update Cycle Status", tags=["Review Cycles"])
def update_cycle_status(
    cycle_id: UUID,
    body: ReviewCycleStatusUpdate,
    db: Session = Depends(get_db),
    actor: CurrentUser = Depends(require_manager_or_admin),
):
    return domain_services.update_cycle_status(db, cycle_id, body.status, actor)


# ── Inputs Router ──────────────────────────────────────────────────────────────

inputs_router = APIRouter()


@inputs_router.post("/{cycle_id}/inputs", response_model=InputResponse, status_code=201,
                    summary="Submit Review Input", tags=["Inputs"])
def submit_input(
    cycle_id: UUID,
    body: InputSubmit,
    db: Session = Depends(get_db),
    actor: CurrentUser = Depends(require_any_authenticated),
):
    return domain_services.submit_input(db, cycle_id, body, actor)


@inputs_router.get("/{cycle_id}/inputs", summary="List Inputs for Cycle", tags=["Inputs"])
def list_inputs(
    cycle_id: UUID,
    db: Session = Depends(get_db),
    actor: CurrentUser = Depends(require_manager_or_admin),
):
    inputs = domain_services.list_inputs_for_cycle(db, cycle_id, actor)
    return [InputResponse.model_validate(i) for i in inputs]


# ── Pipeline Router ────────────────────────────────────────────────────────────

pipeline_router = APIRouter()


@pipeline_router.post(
    "/review-cycles/{cycle_id}/pipeline/trigger",
    response_model=PipelineTriggerResponse,
    status_code=202,
    summary="Trigger AI Pipeline",
    description="Starts the ReviewGuard AI pipeline asynchronously. Returns pipeline_run_id for polling.",
    tags=["Pipeline"],
)
def trigger_pipeline(
    cycle_id: UUID,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    actor: CurrentUser = Depends(require_manager_or_admin),
):
    run_id = pipeline_service.initialize_pipeline(db, str(cycle_id), actor)
    background_tasks.add_task(
        pipeline_service.execute_pipeline,
        pipeline_run_id=run_id,
        review_cycle_id=str(cycle_id),
    )
    return PipelineTriggerResponse(pipeline_run_id=run_id)


@pipeline_router.get(
    "/pipeline/{run_id}/status",
    summary="Get Pipeline Status",
    tags=["Pipeline"],
)
def get_pipeline_status(
    run_id: str,
    actor: CurrentUser = Depends(require_any_authenticated),
):
    return pipeline_service.get_pipeline_status_response(run_id)


# ── Reports Router ─────────────────────────────────────────────────────────────

reports_router = APIRouter()


@reports_router.get(
    "/{report_id}",
    response_model=ReportResponse,
    summary="Get Performance Report",
    description="Returns report with full claims, citations, and bias flags. EMPLOYEE can only see FINALIZED reports.",
    tags=["Reports"],
)
def get_report(
    report_id: UUID,
    db: Session = Depends(get_db),
    actor: CurrentUser = Depends(require_any_authenticated),
):
    report = report_repo.get_with_full_details(db, report_id)
    if not report:
        raise NotFoundError(f"Report {report_id} not found.")

    # EMPLOYEE access gate
    if actor.role == UserRole.EMPLOYEE:
        cycle = report.review_cycle
        if cycle.employee_id != actor.id:
            raise ForbiddenError("You can only view your own reports.")
        from models.enums import ReportStatus
        if report.status != ReportStatus.FINALIZED:
            raise ForbiddenError("Report is not yet finalized.")

    return ReportResponse.model_validate(report)


@reports_router.patch(
    "/{report_id}/status",
    summary="Approval Action",
    description="APPROVE, REVISION_REQUESTED, or REJECT a PENDING_APPROVAL report. Requires idempotency_key.",
    tags=["Reports"],
)
def approval_action(
    report_id: UUID,
    body: ApprovalActionRequest,
    db: Session = Depends(get_db),
    actor: CurrentUser = Depends(require_manager_or_admin),
):
    return pipeline_service.process_approval_action(
        db=db,
        report_id=str(report_id),
        action=body.action,
        reason=body.reason,
        actor=actor,
        idempotency_key=body.idempotency_key,
    )


@reports_router.get(
    "/{report_id}/versions",
    summary="Report Version History",
    tags=["Reports"],
)
def get_report_versions(
    report_id: UUID,
    db: Session = Depends(get_db),
    actor: CurrentUser = Depends(require_manager_or_admin),
):
    report = report_repo.get_by_id(db, report_id)
    if not report:
        raise NotFoundError(f"Report {report_id} not found.")
    versions = report_repo.get_versions_for_cycle(db, report.review_cycle_id)
    return [ReportVersionSummary.model_validate(v) for v in versions]


# ── Audit Router ───────────────────────────────────────────────────────────────

audit_router = APIRouter()


@audit_router.get("", summary="List Audit Events (Admin Only)", tags=["Audit"])
def list_audit_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    actor: CurrentUser = Depends(require_admin),
):
    events = audit_repo.list_recent(db, skip, limit)
    return [AuditEventResponse.model_validate(e) for e in events]


@audit_router.get("/resource/{resource_type}/{resource_id}",
                  summary="Get Events for Resource", tags=["Audit"])
def get_events_for_resource(
    resource_type: str,
    resource_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    actor: CurrentUser = Depends(require_admin),
):
    events = audit_repo.get_by_resource(db, resource_type, resource_id, skip, limit)
    return [AuditEventResponse.model_validate(e) for e in events]


@audit_router.get("/pipeline/{run_id}", summary="Get Events for Pipeline Run", tags=["Audit"])
def get_pipeline_audit(
    run_id: str,
    db: Session = Depends(get_db),
    actor: CurrentUser = Depends(require_admin),
):
    events = audit_repo.get_for_pipeline(db, run_id)
    return [AuditEventResponse.model_validate(e) for e in events]
