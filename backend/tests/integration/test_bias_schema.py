import pytest
from app.ai.agents.bias.validators.schema_validator import SchemaValidator
from app.ai.agents.bias.exceptions import OutputValidationError
from app.ai.agents.bias.schemas import BiasAnalysisSchema

def test_bias_schema_validator_success():
    raw_data = {
        "overall_bias_score": 0.1,
        "risk_level": "LOW",
        "detected_biases": [],
        "unsupported_claims": [],
        "missing_evidence": [],
        "fairness_assessment": "It is fair",
        "confidence": 0.9,
        "summary": "Summary"
    }
    
    parsed = SchemaValidator.validate(raw_data)
    assert isinstance(parsed, BiasAnalysisSchema)
    assert parsed.overall_bias_score == 0.1

def test_bias_schema_validator_missing_fields():
    raw_data = {
        "overall_bias_score": 0.1
    }
    with pytest.raises(ValueError, match="Schema validation failed"):
        SchemaValidator.validate(raw_data)
