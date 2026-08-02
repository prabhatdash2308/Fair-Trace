import pytest
from app.ai.agents.explainability.validators.business_validator import BusinessValidator
from app.ai.agents.explainability.schemas import ExplainabilityAnalysisSchema, ReasoningTrace, TransparencyMetrics, ConfidenceBreakdown
from app.ai.agents.explainability.taxonomy import ExplanationType

def test_explainability_business_validator_bounds():
    schema = ExplainabilityAnalysisSchema.model_construct(
        overall_confidence=1.5, # Invalid
        confidence_breakdown=ConfidenceBreakdown.model_construct(performance=0.9, bias=0.9, reasoning=0.9, overall=0.9),
        reasoning_trace=[], decision_graph=[], evidence_map=[],
        transparency_metrics=TransparencyMetrics.model_construct(
            coverage=1.0, evidence_density=1.0, evidence_consistency=1.0, 
            unsupported_claims_count=0, bias_adjustments_count=0, reasoning_completeness=1.0
        ),
        unsupported_claims=[], audit_summary="ok"
    )
    with pytest.raises(ValueError, match="must be between"):
        BusinessValidator.validate(schema)

def test_explainability_business_validator_missing_evidence():
    trace = ReasoningTrace.model_construct(
        finding="x", explanation_type=ExplanationType.EVIDENCE_BASED,
        reasoning="y", confidence=0.9, evidence_ids=[]
    )
    schema = ExplainabilityAnalysisSchema.model_construct(
        overall_confidence=0.9,
        confidence_breakdown=ConfidenceBreakdown.model_construct(performance=0.9, bias=0.9, reasoning=0.9, overall=0.9),
        reasoning_trace=[trace], decision_graph=[], evidence_map=[],
        transparency_metrics=TransparencyMetrics.model_construct(
            coverage=1.0, evidence_density=1.0, evidence_consistency=1.0, 
            unsupported_claims_count=0, bias_adjustments_count=0, reasoning_completeness=1.0
        ),
        unsupported_claims=[], audit_summary="ok"
    )
    with pytest.raises(ValueError, match="missing evidence IDs"):
        BusinessValidator.validate(schema)
