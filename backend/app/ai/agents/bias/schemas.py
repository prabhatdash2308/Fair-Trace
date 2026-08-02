from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field
import datetime

from app.ai.agents.bias.enums import BiasSeverity, RiskLevel
from app.ai.agents.bias.taxonomy import BiasType
from app.ai.agents.performance.schemas import CostMetrics, AgentMetadata

class DetectedBias(BaseModel):
    """An individual detected bias."""
    category: BiasType = Field(..., description="The category of bias detected.")
    severity: BiasSeverity = Field(..., description="The severity of this specific bias.")
    confidence: float = Field(..., description="Confidence in this detection (0.0 to 1.0).", ge=0.0, le=1.0)
    evidence: List[str] = Field(..., description="Direct quotes from the review supporting this bias detection.")
    evidence_ids: List[str] = Field(default_factory=list, description="IDs or references to the exact chunks where evidence was found.")
    recommendation: str = Field(..., description="Actionable recommendation to resolve the bias.")

class BiasAnalysisSchema(BaseModel):
    """Strict JSON Output Schema requested from the LLM."""
    overall_bias_score: float = Field(..., description="Overall bias risk score (0.0 to 1.0).", ge=0.0, le=1.0)
    risk_level: RiskLevel = Field(..., description="Categorical risk level of the entire review.")
    detected_biases: List[DetectedBias] = Field(default_factory=list, description="List of detected biases.")
    unsupported_claims: List[str] = Field(default_factory=list, description="Claims made in the review without adequate evidence.")
    missing_evidence: List[str] = Field(default_factory=list, description="Specific areas where evidence is notably absent.")
    fairness_assessment: str = Field(..., description="A 1-2 paragraph summary assessing the fairness of the review.")
    confidence: float = Field(..., description="Overall confidence in the bias analysis (0.0 to 1.0).", ge=0.0, le=1.0)
    summary: str = Field(..., description="A high-level executive summary of the findings.")

class BiasAnalysis(BaseModel):
    """The final enriched domain model split across ReviewState."""
    analysis: BiasAnalysisSchema
    cost_metrics: CostMetrics
    metadata: AgentMetadata
