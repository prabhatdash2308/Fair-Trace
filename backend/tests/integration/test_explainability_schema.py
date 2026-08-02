import pytest
from app.ai.agents.explainability.validators.schema_validator import SchemaValidator
from app.ai.agents.explainability.schemas import ExplainabilityAnalysisSchema

def test_explainability_schema_validator_success():
    raw_data = {
        "overall_confidence": 0.9,
        "confidence_breakdown": {"performance": 0.9, "bias": 0.9, "reasoning": 0.9, "overall": 0.9},
        "reasoning_trace": [],
        "decision_graph": [],
        "evidence_map": [],
        "transparency_metrics": {
            "coverage": 1.0, "evidence_density": 1.0, "evidence_consistency": 1.0, 
            "unsupported_claims_count": 0, "bias_adjustments_count": 0, "reasoning_completeness": 1.0
        },
        "unsupported_claims": [],
        "audit_summary": "ok"
    }
    
    parsed = SchemaValidator.validate(raw_data)
    assert isinstance(parsed, ExplainabilityAnalysisSchema)

def test_explainability_schema_validator_missing_fields():
    raw_data = {"overall_confidence": 0.9}
    with pytest.raises(ValueError, match="Schema validation failed"):
        SchemaValidator.validate(raw_data)
