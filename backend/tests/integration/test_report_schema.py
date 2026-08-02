import pytest
from app.ai.agents.report.validators.schema_validator import SchemaValidator
from app.ai.agents.report.schemas import EnterprisePerformanceReportSchema

def test_report_schema_validator_success():
    raw_data = {
        "employee_summary": {},
        "executive_summary": "Excellent.",
        "overall_rating": 4.5,
        "overall_confidence": 0.9,
        "performance_highlights": [],
        "strengths": [],
        "improvement_areas": [],
        "goal_progress": [],
        "development_plan": {"90_day_plan": "do this"},
        "recommended_actions": [{"title": "T", "recommendation": "R", "priority": "HIGH", "impact": "I", "effort": "E", "confidence": 1.0}],
        "risk_summary": {"overall_risk": "low", "bias_risk": "low", "confidence_risk": "low", "missing_evidence": 0, "unsupported_claims": 0},
        "manager_notes": "Good job."
    }
    
    parsed = SchemaValidator.validate(raw_data)
    assert isinstance(parsed, EnterprisePerformanceReportSchema)

def test_report_schema_validator_missing_fields():
    raw_data = {"overall_rating": 4.5}
    with pytest.raises(ValueError, match="Schema validation failed"):
        SchemaValidator.validate(raw_data)
