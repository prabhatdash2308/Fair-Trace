from typing import List, Optional
from pydantic import BaseModel, Field
import datetime

class CostMetrics(BaseModel):
    """Cost accounting for LLM executions."""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    cached_tokens: int = 0
    total_tokens: int = 0
    cost_input: float = 0.0
    cost_output: float = 0.0
    total_cost: float = 0.0

class AgentMetadata(BaseModel):
    """Metadata detailing how this analysis was generated."""
    execution_id: str
    workflow_id: Optional[str] = None
    agent_version: str
    prompt_version: str
    prompt_hash: str
    model: str
    provider: str
    created_at: str = Field(default_factory=lambda: datetime.datetime.now(datetime.UTC).isoformat())
    latency_s: float = 0.0
    retries: int = 0

class Observation(BaseModel):
    """A specific performance observation with evidence."""
    observation: str = Field(..., description="The performance observation.")
    evidence: str = Field(..., description="Direct quote or specific evidence from the context bundle.")
    impact: str = Field(..., description="The impact this behavior had on the organization or team.")

class GoalProgress(BaseModel):
    """Progress on specific goals."""
    goal_name: str = Field(..., description="The name or summary of the goal.")
    status: str = Field(..., description="Current status: e.g., 'Completed', 'On Track', 'At Risk'.")
    notes: str = Field(..., description="Context regarding the progress.")

class PerformanceAnalysisSchema(BaseModel):
    """Strict JSON Output Schema requested from the LLM."""
    overall_score: int = Field(..., description="Overall performance score from 1 to 5.", ge=1, le=5)
    confidence: float = Field(..., description="Confidence level in the analysis from 0.0 to 1.0.", ge=0.0, le=1.0)
    strengths: List[str] = Field(default_factory=list, description="List of key strengths.")
    improvement_areas: List[str] = Field(default_factory=list, description="List of areas needing improvement.")
    key_observations: List[Observation] = Field(default_factory=list, description="Key observations with evidence.")
    goal_progress: List[GoalProgress] = Field(default_factory=list, description="Status of established goals.")
    risk_flags: List[str] = Field(default_factory=list, description="Any identified risks (e.g., flight risk, compliance).")
    analysis_summary: str = Field(..., description="A 2-3 paragraph summary of the employee's performance.")

class PerformanceAnalysis(BaseModel):
    """The final enriched domain model stored in ReviewState."""
    analysis: PerformanceAnalysisSchema
    cost_metrics: CostMetrics
    metadata: AgentMetadata
