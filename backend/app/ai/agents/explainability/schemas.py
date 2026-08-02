from typing import List, Optional
from pydantic import BaseModel, Field

from app.ai.agents.explainability.taxonomy import ExplanationType
from app.ai.agents.performance.schemas import CostMetrics, AgentMetadata

class ConfidenceBreakdown(BaseModel):
    performance: float = Field(..., ge=0.0, le=1.0)
    bias: float = Field(..., ge=0.0, le=1.0)
    reasoning: float = Field(..., ge=0.0, le=1.0)
    overall: float = Field(..., ge=0.0, le=1.0)

class TransparencyMetrics(BaseModel):
    coverage: float = Field(..., ge=0.0, le=1.0)
    evidence_density: float = Field(..., ge=0.0, le=1.0)
    evidence_consistency: float = Field(..., ge=0.0, le=1.0)
    unsupported_claims_count: int = Field(..., ge=0)
    bias_adjustments_count: int = Field(..., ge=0)
    reasoning_completeness: float = Field(..., ge=0.0, le=1.0)

class UnsupportedClaim(BaseModel):
    claim: str = Field(...)
    reason: str = Field(...)
    recommended_action: str = Field(...)

class DecisionNode(BaseModel):
    node: str = Field(...)
    inputs: List[str] = Field(default_factory=list)
    outputs: List[str] = Field(default_factory=list)

class ReasoningTrace(BaseModel):
    finding: str = Field(...)
    explanation_type: ExplanationType = Field(...)
    reasoning: str = Field(...)
    confidence: float = Field(..., ge=0.0, le=1.0)
    evidence_ids: List[str] = Field(default_factory=list)

class ExplainabilityAnalysisSchema(BaseModel):
    """Strict JSON Output Schema requested from the LLM."""
    overall_confidence: float = Field(..., ge=0.0, le=1.0)
    confidence_breakdown: ConfidenceBreakdown
    reasoning_trace: List[ReasoningTrace] = Field(default_factory=list)
    decision_graph: List[DecisionNode] = Field(default_factory=list)
    evidence_map: List[str] = Field(default_factory=list) # e.g. mapping strings or objects
    transparency_metrics: TransparencyMetrics
    unsupported_claims: List[UnsupportedClaim] = Field(default_factory=list)
    audit_summary: str = Field(...)

class ExplainabilityAnalysis(BaseModel):
    """The final enriched domain model split across ReviewState."""
    analysis: ExplainabilityAnalysisSchema
    cost_metrics: CostMetrics
    metadata: AgentMetadata
