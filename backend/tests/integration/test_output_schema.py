import pytest
from app.ai.agents.performance.validators.schema_validator import SchemaValidator
from app.ai.agents.performance.validators.business_validator import BusinessValidator
from app.ai.agents.performance.exceptions import OutputValidationError
from app.ai.agents.performance.schemas import PerformanceAnalysisSchema

def test_schema_validator_success():
    raw_data = {
        "overall_score": 4,
        "confidence": 0.8,
        "strengths": ["Leadership"],
        "improvement_areas": [],
        "key_observations": [{"observation": "Led project", "evidence": "Led X", "impact": "High"}],
        "goal_progress": [],
        "risk_flags": [],
        "analysis_summary": "A very long summary text goes here."
    }
    
    parsed = SchemaValidator.validate(raw_data)
    assert isinstance(parsed, PerformanceAnalysisSchema)
    assert parsed.overall_score == 4

def test_schema_validator_missing_fields():
    raw_data = {
        "overall_score": 4
    }
    with pytest.raises(OutputValidationError, match="validation failed"):
        SchemaValidator.validate(raw_data)

def test_business_validator_score_bounds():
    # model_construct bypasses Pydantic's built-in validation (ge=1, le=5) to let us test business logic fallback
    schema = PerformanceAnalysisSchema.model_construct(
        overall_score=6,
        confidence=0.8,
        strengths=[], improvement_areas=[],
        key_observations=[{"observation": "x", "evidence": "y", "impact": "z"}],
        goal_progress=[], risk_flags=[],
        analysis_summary="This is a summary of at least fifty characters long."
    )
    with pytest.raises(OutputValidationError, match="overall_score must be between 1 and 5"):
        BusinessValidator.validate(schema)

def test_business_validator_duplicate_evidence():
    schema = PerformanceAnalysisSchema(
        overall_score=4,
        confidence=0.8,
        strengths=[], improvement_areas=[],
        key_observations=[
            {"observation": "x1", "evidence": "same quote", "impact": "z1"},
            {"observation": "x2", "evidence": "same quote", "impact": "z2"}
        ],
        goal_progress=[], risk_flags=[],
        analysis_summary="This is a summary of at least fifty characters long."
    )
    with pytest.raises(OutputValidationError, match="Duplicate evidence"):
        BusinessValidator.validate(schema)

def test_business_validator_short_summary():
    schema = PerformanceAnalysisSchema(
        overall_score=4,
        confidence=0.8,
        strengths=[], improvement_areas=[],
        key_observations=[{"observation": "x", "evidence": "y", "impact": "z"}],
        goal_progress=[], risk_flags=[],
        analysis_summary="Too short."
    )
    with pytest.raises(OutputValidationError, match="least 50 characters long"):
        BusinessValidator.validate(schema)
