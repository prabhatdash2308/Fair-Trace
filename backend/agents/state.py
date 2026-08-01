"""
ReviewGuard AI — LangGraph Pipeline State
Complete TypedDict with all fields owned by each agent.
State versioning (Improvement #5): state_version increments after each agent write.
"""

from __future__ import annotations

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
