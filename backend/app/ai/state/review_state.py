from __future__ import annotations
"""
ReviewGuard AI - Master State Definition
Single Source of Truth for the entire AI pipeline.
"""
from enum import Enum
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from pydantic.types import UUID4
from datetime import datetime, timezone
import uuid

# =========================================================
# ENUMS
# =========================================================

class PipelineStatus(str, Enum):
    """Pipeline execution status."""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    HALTED = "HALTED"
    AWAITING_HUMAN = "AWAITING_HUMAN"

class ApprovalStatus(str, Enum):
    """Human approval status."""
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REVISION_REQUESTED = "REVISION_REQUESTED"
    REJECTED = "REJECTED"

class BiasSeverity(str, Enum):
    """Severity level of detected bias."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class BiasType(str, Enum):
    """Types of bias that can be detected."""
    RECENCY = "RECENCY"
    HALO = "HALO"
    HORN = "HORN"
    LENIENCY = "LENIENCY"
    SEVERITY = "SEVERITY"
    GENDER = "GENDER"
    AGE = "AGE"
    UNSUPPORTED = "UNSUPPORTED"
    IMBALANCE = "IMBALANCE"

class ExecutionStatus(str, Enum):
    """Status of an individual execution step or agent."""
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"

# =========================================================
# MODELS
# =========================================================

class MetadataState(BaseModel):
    """
    Owned by: Graph / Orchestrator
    Purpose: Core identifiers and lifecycle tracking for the pipeline run.
    Meaning: Holds IDs linking back to the database and current pipeline status.
    """
    review_cycle_id: Optional[UUID4] = None
    employee_id: Optional[UUID4] = None
    manager_id: Optional[UUID4] = None
    pipeline_id: UUID4 = Field(default_factory=uuid.uuid4)
    correlation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    current_agent: Optional[str] = None
    pipeline_status: PipelineStatus = PipelineStatus.PENDING
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None

class InputState(BaseModel):
    """
    Owned by: Intake Agent
    Purpose: Holds all raw and validated feedback inputs.
    Meaning: The source materials for the performance review.
    """
    self_assessment: Optional[str] = None
    manager_feedback: Optional[str] = None
    peer_feedback: List[str] = Field(default_factory=list)
    meeting_notes: List[str] = Field(default_factory=list)
    project_outcomes: List[str] = Field(default_factory=list)
    goals: List[str] = Field(default_factory=list)
    uploaded_documents: List[str] = Field(default_factory=list)

class RetrievalState(BaseModel):
    """
    Owned by: Embedding Agent / Evidence Retrieval Agent
    Purpose: Stores state related to vector search and RAG operations.
    Meaning: Keeps track of what was searched and what was found.
    """
    # Embedding Agent Fields
    embedded_documents: List[str] = Field(default_factory=list)
    total_chunks: int = Field(default=0, ge=0)
    vector_ids: List[str] = Field(default_factory=list)
    collection_name: Optional[str] = None
    embedding_dimension: Optional[int] = None
    embedding_cost: float = Field(default=0.0, ge=0.0)
    embedding_latency: int = Field(default=0, ge=0)
    status: str = "pending"
    
    # Evidence Retrieval Agent Fields
    retrieval_queries: List[str] = Field(default_factory=list)
    retrieved_chunks: List[str] = Field(default_factory=list)
    retrieval_scores: List[float] = Field(default_factory=list)
    retrieval_metadata: List[Dict[str, Any]] = Field(default_factory=list)

class EvidenceState(BaseModel):
    """
    Owned by: Evidence Retrieval Agent
    Purpose: Curated evidence mapped to specific performance dimensions.
    Meaning: Synthesized facts and citations used to ground claims.
    """
    retrieved_chunks: List[str] = Field(default_factory=list)
    retrieved_documents: List[str] = Field(default_factory=list)
    citations: List[str] = Field(default_factory=list)
    similarity_scores: List[float] = Field(default_factory=list)
    evidence_count: int = Field(default=0, ge=0)
    retrieval_latency_ms: int = Field(default=0, ge=0)
    retrieval_cost: float = Field(default=0.0, ge=0.0)
    top_matches: List[Dict[str, Any]] = Field(default_factory=list)
    status: str = "pending"
    
    # Legacy fields
    evidence_list: List[str] = Field(default_factory=list)
    evidence_strength: float = Field(default=0.0, ge=0.0, le=100.0)
    supporting_sources: List[str] = Field(default_factory=list)

class BiasFinding(BaseModel):
    bias_type: BiasType
    severity: BiasSeverity
    confidence: float
    reason: str
    recommendation: str
    supporting_citations: List[str]

class BiasState(BaseModel):
    """
    Owned by: Bias Detection Agent
    Purpose: Tracks detected biases and mitigation recommendations.
    Meaning: Ensures fairness by flagging problematic language or unsupported claims.
    """
    findings: List[BiasFinding] = Field(default_factory=list)
    status: str = "pending"
    
    # Legacy fields
    bias_flags: List[str] = Field(default_factory=list)
    bias_types: List[BiasType] = Field(default_factory=list)
    bias_score: float = Field(default=0.0, ge=0.0, le=100.0)
    bias_explanations: List[str] = Field(default_factory=list)
    missing_feedback: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)

class AnalysisState(BaseModel):
    """
    Owned by: Performance Analysis Agent
    Purpose: Synthesized evaluation of the employee's performance.
    Meaning: Core analytical results based on the evidence.
    """
    strengths: List[str] = Field(default_factory=list)
    growth_areas: List[str] = Field(default_factory=list)
    achievements: List[str] = Field(default_factory=list)
    goal_progress: str = ""
    risks: List[str] = Field(default_factory=list)
    overall_rating: Optional[str] = None

class ReportState(BaseModel):
    """
    Owned by: Report Generation Agent
    Purpose: The final output artifacts to be presented to the user.
    Meaning: Drafts and final versions of the performance review documents.
    """
    executive_summary: str = ""
    employee_summary: str = ""
    manager_summary: str = ""
    final_report: str = ""
    confidence_score: float = Field(default=0.0, ge=0.0, le=100.0)

class ApprovalState(BaseModel):
    """
    Owned by: Human Approval Agent
    Purpose: Tracks the human-in-the-loop review process.
    Meaning: Ensures human oversight before finalizing the review.
    """
    approval_status: ApprovalStatus = ApprovalStatus.PENDING
    approved_by: Optional[UUID4] = None
    approved_at: Optional[datetime] = None
    reviewer_comments: str = ""

class AuditState(BaseModel):
    """
    Owned by: Audit Agent
    Purpose: Observability and compliance tracking.
    Meaning: Logs of agent actions, token costs, and system performance.
    """
    agent_logs: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    latency_ms: int = Field(default=0, ge=0)
    token_usage: int = Field(default=0, ge=0)
    estimated_cost: float = Field(default=0.0, ge=0.0)

class ExecutionState(BaseModel):
    """
    Owned by: Graph / Orchestrator
    Purpose: Control flow tracking for the LangGraph pipeline.
    Meaning: Maintains the state machine of which steps have completed.
    """
    current_step: Optional[str] = None
    completed_steps: List[str] = Field(default_factory=list)
    failed_steps: List[str] = Field(default_factory=list)
    retry_count: int = Field(default=0, ge=0)

class ReviewState(BaseModel):
    """
    Owned by: LangGraph Shared Memory
    Purpose: The Single Source of Truth for the entire AI pipeline.
    Meaning: Composes all sub-states into a single, strongly-typed, serializable object.
    """
    metadata: MetadataState = Field(default_factory=MetadataState)
    input: InputState = Field(default_factory=InputState)
    retrieval: RetrievalState = Field(default_factory=RetrievalState)
    evidence: EvidenceState = Field(default_factory=EvidenceState)
    bias: BiasState = Field(default_factory=BiasState)
    analysis: AnalysisState = Field(default_factory=AnalysisState)
    report: ReportState = Field(default_factory=ReportState)
    approval: ApprovalState = Field(default_factory=ApprovalState)
    audit: AuditState = Field(default_factory=AuditState)
    execution: ExecutionState = Field(default_factory=ExecutionState)

# =========================================================
# LEGACY STATE (Kept to prevent import errors during refactor)
# =========================================================


from typing import Annotated, Optional, TypedDict
import operator
"""
ReviewGuard AI — LangGraph Pipeline State
Complete TypedDict with all fields owned by each agent.
State versioning (Improvement #5): state_version increments after each agent write.
"""



import operator
from typing import Annotated, Optional, TypedDict


# ── Sub-Object Definitions ─────────────────────────────────────────────────────

class ValidatedInput(TypedDict):
    input_id: str
    input_type: str
    content_text: str
    submitted_by_id: str
    submitted_at: str
    is_anonymized: bool
    char_count: int
    submission_week: int


class EvidenceCitationState(TypedDict):
    citation_id: str
    source_input_id: str
    source_input_type: str
    extracted_passage: str
    similarity_score: float
    retrieval_rank: int
    query_dimension: str


class PerformanceClaimState(TypedDict):
    claim_id: str
    dimension: str
    claim_text: str
    explanation: str
    confidence: str
    evidence_citation_ids: list[str]
    is_supported: bool
    display_order: int


class BiasFlagState(TypedDict):
    flag_id: str
    bias_type: str
    severity: str
    affected_text: Optional[str]
    source_input_id: Optional[str]
    recommended_action: str
    detected_by_agent: str
    detection_reasoning: str


class AgentExecutionRecord(TypedDict):
    agent_name: str
    start_time: str
    end_time: Optional[str]
    status: str
    output_summary: str
    error_message: Optional[str]
    items_processed: int
    # Observability fields (Improvements #2, #4, #7)
    llm_model_used: Optional[str]
    tokens_prompt: Optional[int]
    tokens_completion: Optional[int]
    tokens_total: Optional[int]
    estimated_cost_usd: Optional[float]
    latency_ms: Optional[int]
    prompt_name: Optional[str]
    prompt_version: Optional[str]
    correlation_id: Optional[str]
    llm_request_id: Optional[str]


class StakeholderDistribution(TypedDict):
    self_assessment_pct: float
    manager_note_pct: float
    peer_review_pct: float
    project_outcome_pct: float
    goal_pct: float
    meeting_note_pct: float
    dominant_source: str
    is_imbalanced: bool


class ConfidenceResult(TypedDict):
    score: str
    numeric_score: float
    evidence_quantity_score: float
    evidence_quality_score: float
    bias_flag_penalty: float
    stakeholder_coverage_score: float
    explanation: str


class ExplanationTrace(TypedDict):
    claim_id: str
    step_1_evidence_found: str
    step_2_evidence_quality: str
    step_3_synthesis: str
    step_4_bias_check: str
    step_5_conclusion: str


# ── Master Pipeline State ──────────────────────────────────────────────────────

class ReviewGuardState(TypedDict):

    # Pipeline Identity
    pipeline_run_id: str
    state_version: int                          # Incremented by each agent (Improvement #5)
    review_cycle_id: str
    employee_id: str
    manager_id: str
    triggered_by_id: str
    correlation_id: str                         # Equals pipeline_run_id (Improvement #7)

    # Input Processing — Intake Agent writes
    raw_input_ids: list[str]
    validated_inputs: list[ValidatedInput]
    intake_complete: bool
    intake_warnings: list[str]

    # Embedding — Embedding Agent writes
    qdrant_collection_name: str               # Always "reviewguard_documents" (Improvement #1)
    embedded_input_ids: list[str]
    total_chunks_created: int
    embedding_complete: bool

    # Evidence — Evidence Retrieval Agent writes
    evidence_index: list[EvidenceCitationState]
    evidence_by_dimension: dict               # {dimension: [EvidenceCitationState]}
    evidence_ready: bool                       # P1 gate
    low_evidence_dimensions: list[str]

    # Bias Detection — Bias Detection Agent writes
    bias_flags: list[BiasFlagState]
    stakeholder_distribution: Optional[StakeholderDistribution]
    high_bias_count: int
    medium_bias_count: int
    bias_detection_complete: bool

    # Performance Analysis — Performance Analysis Agent writes
    dimension_summaries: dict                  # {dimension: "synthesis text"}
    analysis_complete: bool
    confidence_result: Optional[ConfidenceResult]

    # Report Generation — Report Generation Agent writes
    performance_claims: list[PerformanceClaimState]
    evidence_citations: list[EvidenceCitationState]
    executive_summary: Optional[str]
    recommended_actions: list[str]
    report_db_id: Optional[str]
    report_version: int
    report_complete: bool

    # Explainability — Explainability Agent writes
    explanation_traces: list[ExplanationTrace]
    evaluation_metrics: dict
    explainability_complete: bool

    # Human Approval — Human Approval Agent writes/reads
    approval_required: bool
    approval_status: str                       # PENDING | APPROVED | REVISION_REQUESTED | REJECTED
    approval_actor_id: Optional[str]
    approval_reason: Optional[str]
    approval_timestamp: Optional[str]
    approval_idempotency_key: Optional[str]    # Improvement #8

    # Audit — all agents append (operator.add prevents overwrite)
    agent_executions: Annotated[list[AgentExecutionRecord], operator.add]
    pipeline_total_tokens: int                 # Running sum (Improvement #2)
    pipeline_total_cost_usd: float             # Running sum (Improvement #2)

    # Pipeline Control
    pipeline_status: str                       # RUNNING | COMPLETED | FAILED | HALTED | AWAITING_HUMAN
    current_agent: str
    error_state: Optional[dict]
    created_at: str
    completed_at: Optional[str]