import pytest
from unittest.mock import AsyncMock, patch
from app.ai.agents.bias.service import BiasAnalysisService

@pytest.mark.asyncio
async def test_bias_analyze_context_missing_fields():
    with pytest.raises(ValueError, match="Execution ID is missing"):
        await BiasAnalysisService.analyze_context({"context_bundle": {}, "performance_analysis": {}})
        
    with pytest.raises(ValueError, match="Context bundle is missing"):
        await BiasAnalysisService.analyze_context({"execution_id": "123", "performance_analysis": {}})
        
    with pytest.raises(ValueError, match="Performance analysis is missing"):
        await BiasAnalysisService.analyze_context({"execution_id": "123", "context_bundle": {"data": "test"}})

@pytest.mark.asyncio
@patch("app.ai.agents.bias.service.BiasAgent.analyze", new_callable=AsyncMock)
@patch("app.ai.agents.bias.service.emit_bias_telemetry")
@patch("app.ai.agents.bias.service.log_prompt_snapshot")
async def test_bias_analyze_context_success(mock_snapshot, mock_telemetry, mock_analyze):
    from app.ai.agents.bias.schemas import BiasAnalysis, BiasAnalysisSchema, AgentMetadata
    from app.ai.agents.performance.schemas import CostMetrics
    from app.ai.agents.bias.enums import RiskLevel
    
    mock_analyze.return_value = BiasAnalysis(
        analysis=BiasAnalysisSchema(
            overall_bias_score=0.1,
            risk_level=RiskLevel.LOW,
            detected_biases=[],
            unsupported_claims=[],
            missing_evidence=[],
            fairness_assessment="ok",
            confidence=0.9,
            summary="ok"
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
        "workflow_id": "wf-1"
    }
    
    result = await BiasAnalysisService.analyze_context(state)
    
    assert result["analysis"]["overall_bias_score"] == 0.1
    mock_telemetry.assert_called_once()
    mock_snapshot.assert_called_once()
