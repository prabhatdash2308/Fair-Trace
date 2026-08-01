import json
from pathlib import Path

file_path = Path("backend/app/ai/state/review_state.py")
if file_path.exists():
    legacy_content = file_path.read_text(encoding="utf-8")
else:
    legacy_content = ""

new_content = '''"""
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
    citations: List[str] = Field(default_factory=list)
    evidence_list: List[str] = Field(default_factory=list)
    evidence_strength: float = Field(default=0.0, ge=0.0, le=100.0)
    supporting_sources: List[str] = Field(default_factory=list)

class BiasState(BaseModel):
    """
    Owned by: Bias Detection Agent
    Purpose: Tracks detected biases and mitigation recommendations.
    Meaning: Ensures fairness by flagging problematic language or unsupported claims.
    """
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

'''

# Remove the initial import statements from the legacy content if it exists
legacy_lines = legacy_content.splitlines()
cleaned_legacy = []
for line in legacy_lines:
    if line.startswith("from __future__") or "import " in line:
        pass
    cleaned_legacy.append(line)

legacy_joined = "\n".join(cleaned_legacy)
# Re-add necessary legacy imports just in case
legacy_imports = """
from typing import Annotated, Optional, TypedDict
import operator
"""

file_path.write_text(new_content + legacy_imports + legacy_joined, encoding="utf-8")
print("Done writing review_state.py")
