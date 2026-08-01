"""ReviewGuard AI — All Pydantic Request/Response Schemas"""

from __future__ import annotations

from datetime import date, datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from models.enums import (
    ApprovalAction,
    BiasType,
    ConfidenceLevel,
    InputType,
    PerformanceDimension,
    ReportStatus,
    ReviewCycleStatus,
    Severity,
    UserRole,
)


# ── Shared Config ──────────────────────────────────────────────────────────────
class OrmBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ── Auth ───────────────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserBrief(OrmBase):
    id: UUID
    email: str
    full_name: str
    role: UserRole


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds
    user: UserBrief


# ── Users ──────────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=255)
    full_name: str = Field(..., min_length=2, max_length=255)
    role: UserRole
    manager_id: UUID | None = None


class UserResponse(OrmBase):
    id: UUID
    email: str
    full_name: str
    role: UserRole
    manager_id: UUID | None
    is_active: bool
    created_at: datetime


class UserUpdate(BaseModel):
    full_name: str | None = Field(None, min_length=2, max_length=255)
    is_active: bool | None = None
    manager_id: UUID | None = None


# ── Review Cycles ──────────────────────────────────────────────────────────────

class ReviewCycleCreate(BaseModel):
    employee_id: UUID
    title: str = Field(..., min_length=2, max_length=255)
    review_period_start: date
    review_period_end: date


class ReviewCycleStatusUpdate(BaseModel):
    status: ReviewCycleStatus


class ReviewCycleResponse(OrmBase):
    id: UUID
    employee_id: UUID
    manager_id: UUID
    title: str
    review_period_start: date
    review_period_end: date
    status: ReviewCycleStatus
    created_at: datetime
    updated_at: datetime


class PaginatedReviewCycles(BaseModel):
    items: list[ReviewCycleResponse]
    total: int
    skip: int
    limit: int
    has_more: bool


# ── Review Inputs ──────────────────────────────────────────────────────────────

class InputSubmit(BaseModel):
    input_type: InputType
    content_text: str = Field(..., min_length=50, max_length=10000)
    is_anonymized: bool = False


class InputResponse(OrmBase):
    id: UUID
    review_cycle_id: UUID
    input_type: InputType
    content_text: str
    is_anonymized: bool
    submitted_at: datetime


# ── Pipeline ───────────────────────────────────────────────────────────────────

class PipelineTriggerResponse(BaseModel):
    pipeline_run_id: str
    status: str = "QUEUED"
    message: str = "Pipeline triggered successfully. Poll /pipeline/{run_id}/status for updates."


class AgentExecutionResponse(BaseModel):
    agent_name: str
    status: str
    start_time: str
    end_time: str | None = None
    output_summary: str
    error_message: str | None = None
    latency_ms: int | None = None
    tokens_total: int | None = None
    estimated_cost_usd: float | None = None
    llm_model_used: str | None = None
    prompt_version: str | None = None


class PipelineStatusResponse(BaseModel):
    pipeline_run_id: str
    review_cycle_id: str
    pipeline_status: str
    current_agent: str
    agent_executions: list[AgentExecutionResponse]
    pipeline_total_tokens: int | None = None
    pipeline_total_cost_usd: float | None = None
    created_at: str
    completed_at: str | None = None
    error_state: dict | None = None


# ── Reports ────────────────────────────────────────────────────────────────────

class CitationResponse(OrmBase):
    id: UUID
    review_input_id: UUID
    extracted_passage: str
    similarity_score: float
    retrieval_rank: int


class ClaimResponse(OrmBase):
    id: UUID
    dimension: PerformanceDimension
    claim_text: str
    explanation: str
    confidence: ConfidenceLevel
    is_supported: bool
    display_order: int
    citations: list[CitationResponse] = []


class BiasFlagResponse(OrmBase):
    id: UUID
    bias_type: BiasType
    severity: Severity
    affected_text: str | None = None
    recommended_action: str
    detection_reasoning: str
    detected_at: datetime


class ReportResponse(OrmBase):
    id: UUID
    review_cycle_id: UUID
    version: int
    status: ReportStatus
    executive_summary: str | None = None
    recommended_actions: list[str] | None = None
    confidence_score: ConfidenceLevel | None = None
    confidence_explanation: str | None = None
    approved_by: UUID | None = None
    approved_at: datetime | None = None
    approval_reason: str | None = None
    claims: list[ClaimResponse] = []
    bias_flags: list[BiasFlagResponse] = []
    generated_at: datetime
    pipeline_run_id: str


class ReportVersionSummary(OrmBase):
    id: UUID
    version: int
    status: ReportStatus
    confidence_score: ConfidenceLevel | None = None
    generated_at: datetime
    is_current: bool


class ApprovalActionRequest(BaseModel):
    action: ApprovalAction
    reason: str = Field(..., min_length=10, max_length=2000)
    idempotency_key: str = Field(..., min_length=36, max_length=36)


# ── Audit ──────────────────────────────────────────────────────────────────────

class AuditEventResponse(OrmBase):
    id: UUID
    event_type: str
    actor_id: UUID | None = None
    actor_role: UserRole | None = None
    resource_type: str
    resource_id: UUID
    event_payload: dict
    occurred_at: datetime
    correlation_id: str | None = None
    state_version: int | None = None
    prompt_version: str | None = None


# ── Health ─────────────────────────────────────────────────────────────────────

class HealthResponse(BaseModel):
    status: str
    version: str
    services: dict[str, bool]
