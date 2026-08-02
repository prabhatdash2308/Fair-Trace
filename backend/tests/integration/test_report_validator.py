import pytest
from app.ai.agents.report.validators.business_validator import BusinessValidator
from app.ai.agents.report.schemas import EnterprisePerformanceReportSchema, DevelopmentPlan, RiskSummary, Recommendation, Priority

def test_report_business_validator_bounds():
    schema = EnterprisePerformanceReportSchema.model_construct(
        employee_summary={}, executive_summary="", overall_rating=6.0, # Invalid
        overall_confidence=0.9, performance_highlights=[], strengths=[], improvement_areas=[], goal_progress=[],
        development_plan=DevelopmentPlan.model_construct(plan_90_day="a"),
        recommended_actions=[], risk_summary=RiskSummary.model_construct(overall_risk="low", bias_risk="low", confidence_risk="low", missing_evidence=0, unsupported_claims=0), manager_notes=""
    )
    with pytest.raises(ValueError, match="must be between 1.0 and 5.0"):
        BusinessValidator.validate(schema)

def test_report_business_validator_duplicate_recommendations():
    rec = Recommendation.model_construct(title="Improve", recommendation="A", priority=Priority.HIGH, impact="H", effort="L", confidence=0.9, evidence_ids=[])
    schema = EnterprisePerformanceReportSchema.model_construct(
        employee_summary={}, executive_summary="", overall_rating=4.0, overall_confidence=0.9, performance_highlights=[], strengths=[], improvement_areas=[], goal_progress=[],
        development_plan=DevelopmentPlan.model_construct(plan_90_day="a"),
        recommended_actions=[rec, rec], # Duplicate
        risk_summary=RiskSummary.model_construct(overall_risk="low", bias_risk="low", confidence_risk="low", missing_evidence=0, unsupported_claims=0), manager_notes=""
    )
    with pytest.raises(ValueError, match="Duplicate recommended actions"):
        BusinessValidator.validate(schema)
