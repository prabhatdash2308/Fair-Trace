import pytest
from app.ai.agents.bias.validators.business_validator import BusinessValidator
from app.ai.agents.bias.schemas import BiasAnalysisSchema, DetectedBias
from app.ai.agents.bias.enums import RiskLevel, BiasSeverity
from app.ai.agents.bias.taxonomy import BiasType

def test_bias_business_validator_score_bounds():
    schema = BiasAnalysisSchema.model_construct(
        overall_bias_score=1.5, # Invalid!
        risk_level=RiskLevel.LOW,
        detected_biases=[], unsupported_claims=[], missing_evidence=[],
        fairness_assessment="X", confidence=0.9, summary="Y"
    )
    with pytest.raises(ValueError, match="overall_bias_score must be between"):
        BusinessValidator.validate(schema)

def test_bias_business_validator_magic_zero():
    bias = DetectedBias.model_construct(
        category=BiasType.RECENCY, severity=BiasSeverity.HIGH,
        confidence=0.9, evidence=[], evidence_ids=[], recommendation="x"
    )
    schema = BiasAnalysisSchema.model_construct(
        overall_bias_score=0.0,
        risk_level=RiskLevel.LOW,
        detected_biases=[bias], unsupported_claims=[], missing_evidence=[],
        fairness_assessment="X", confidence=0.9, summary="Y"
    )
    with pytest.raises(ValueError, match="cannot be 0.0 when biases are detected"):
        BusinessValidator.validate(schema)

def test_bias_business_validator_duplicate_evidence():
    bias = DetectedBias.model_construct(
        category=BiasType.RECENCY, severity=BiasSeverity.HIGH,
        confidence=0.9, evidence=[], evidence_ids=["chunk_1", "chunk_1"], recommendation="x"
    )
    schema = BiasAnalysisSchema.model_construct(
        overall_bias_score=0.5,
        risk_level=RiskLevel.MEDIUM,
        detected_biases=[bias], unsupported_claims=[], missing_evidence=[],
        fairness_assessment="X", confidence=0.9, summary="Y"
    )
    with pytest.raises(ValueError, match="Duplicate evidence_ids"):
        BusinessValidator.validate(schema)
