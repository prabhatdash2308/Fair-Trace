from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum
from app.ai.agents.performance.schemas import CostMetrics, AgentMetadata

class Priority(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class Recommendation(BaseModel):
    title: str = Field(...)
    recommendation: str = Field(...)
    priority: Priority = Field(...)
    impact: str = Field(...)
    effort: str = Field(...)
    evidence_ids: List[str] = Field(default_factory=list)
    confidence: float = Field(..., ge=0.0, le=1.0)

class GoalProgress(BaseModel):
    goal_name: str = Field(...)
    status: str = Field(...)
    progress_percentage: int = Field(..., ge=0, le=100)
    manager_assessment: str = Field(...)

class DevelopmentPlan(BaseModel):
    plan_90_day: str = Field(alias="90_day_plan")
    learning_goals: List[str] = Field(default_factory=list)
    manager_actions: List[str] = Field(default_factory=list)
    employee_actions: List[str] = Field(default_factory=list)
    success_metrics: List[str] = Field(default_factory=list)
    model_config = {"populate_by_name": True}
    
class RiskSummary(BaseModel):
    overall_risk: str = Field(...)
    bias_risk: str = Field(...)
    confidence_risk: str = Field(...)
    missing_evidence: int = Field(..., ge=0)
    unsupported_claims: int = Field(..., ge=0)

class AuditSummary(BaseModel):
    performance_confidence: float = Field(...)
    bias_summary: str = Field(...)
    explainability_coverage: float = Field(...)
    evidence_count: int = Field(...)
    prompt_version: str = Field(...)
    prompt_hash: str = Field(...)
    model: str = Field(...)
    execution_id: str = Field(...)
    workflow_id: str = Field(...)
    generated_at: str = Field(...)

class ReportMetadata(BaseModel):
    report_version: str = Field(...)
    schema_version: str = Field(...)
    prompt_version: str = Field(...)
    prompt_hash: str = Field(...)
    provider: str = Field(...)
    model: str = Field(...)
    execution_id: str = Field(...)
    workflow_id: str = Field(...)
    generated_at: str = Field(...)

class EnterprisePerformanceReportSchema(BaseModel):
    """The strict JSON Output Schema requested from the LLM."""
    employee_summary: dict = Field(default_factory=dict)
    executive_summary: str = Field(...)
    overall_rating: float = Field(...)
    overall_confidence: float = Field(..., ge=0.0, le=1.0)
    performance_highlights: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    improvement_areas: List[str] = Field(default_factory=list)
    goal_progress: List[GoalProgress] = Field(default_factory=list)
    development_plan: DevelopmentPlan = Field(...)
    recommended_actions: List[Recommendation] = Field(default_factory=list)
    risk_summary: RiskSummary = Field(...)
    manager_notes: str = Field(...)

class PipelineMetrics(BaseModel):
    total_pipeline_cost: float = Field(..., ge=0.0)
    total_tokens: int = Field(..., ge=0)
    report_length: int = Field(..., ge=0)
    recommendation_count: int = Field(..., ge=0)
    strength_count: int = Field(..., ge=0)
    improvement_count: int = Field(..., ge=0)
    evidence_count: int = Field(..., ge=0)
    risk_count: int = Field(..., ge=0)
    overall_score: float = Field(...)
    confidence: float = Field(..., ge=0.0, le=1.0)

class EnterprisePerformanceReport(BaseModel):
    """The final enriched domain model injected into state.final_report."""
    report: EnterprisePerformanceReportSchema
    audit_summary: AuditSummary
    pipeline_metrics: PipelineMetrics
    cost_metrics: CostMetrics
    metadata: ReportMetadata
