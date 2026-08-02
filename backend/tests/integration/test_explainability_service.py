import pytest
from unittest.mock import AsyncMock, patch
from app.ai.agents.explainability.service import ExplainabilityAnalysisService

@pytest.mark.asyncio
async def test_explainability_analyze_context_missing_fields():
    with pytest.raises(ValueError, match="Execution ID is missing"):
        await ExplainabilityAnalysisService.analyze_context({"context_bundle": {}, "performance_analysis": {}, "bias_analysis": {}})

@pytest.mark.asyncio
@patch("app.ai.agents.explainability.service.ExplainabilityAgent.analyze", new_callable=AsyncMock)
@patch("app.ai.agents.explainability.service.emit_explainability_telemetry")
@patch("app.ai.agents.explainability.service.log_prompt_snapshot")
async def test_explainability_analyze_context_success(mock_snapshot, mock_telemetry, mock_analyze):
    from app.ai.agents.explainability.schemas import ExplainabilityAnalysis, ExplainabilityAnalysisSchema, AgentMetadata, ConfidenceBreakdown, TransparencyMetrics
    from app.ai.agents.performance.schemas import CostMetrics
    
    mock_analyze.return_value = ExplainabilityAnalysis(
        analysis=ExplainabilityAnalysisSchema(
            overall_confidence=0.9,
            confidence_breakdown=ConfidenceBreakdown.model_construct(performance=0.9, bias=0.9, reasoning=0.9, overall=0.9),
            reasoning_trace=[], decision_graph=[], evidence_map=[],
            transparency_metrics=TransparencyMetrics.model_construct(
                coverage=1.0, evidence_density=1.0, evidence_consistency=1.0, 
                unsupported_claims_count=0, bias_adjustments_count=0, reasoning_completeness=1.0
            ),
            unsupported_claims=[], audit_summary="ok"
        ),
        cost_metrics=CostMetrics(),
        metadata=AgentMetadata(
            execution_id="123", agent_version="1.0", prompt_version="1.0",
            prompt_hash="xyz", model="gpt-4o", provider="openai"
        )
    )
    
    state = {
        "execution_id": "123",
        "context_bundle": {"data": "test"},
        "performance_analysis": {"data": "test2"},
        "bias_analysis": {"data": "test3"},
        "workflow_id": "wf-1"
    }
    
    result = await ExplainabilityAnalysisService.analyze_context(state)
    
    assert result["analysis"]["overall_confidence"] == 0.9
    mock_telemetry.assert_called_once()
    mock_snapshot.assert_called_once()
