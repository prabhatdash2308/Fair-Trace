import pytest
from unittest.mock import AsyncMock, patch
from app.ai.agents.performance.service import PerformanceAnalysisService

@pytest.mark.asyncio
async def test_analyze_context_missing_fields():
    with pytest.raises(ValueError, match="Execution ID is missing"):
        await PerformanceAnalysisService.analyze_context({"context_bundle": {}})
        
    with pytest.raises(ValueError, match="Context bundle is missing"):
        await PerformanceAnalysisService.analyze_context({"execution_id": "123"})

@pytest.mark.asyncio
@patch("app.ai.agents.performance.service.PerformanceAgent.analyze", new_callable=AsyncMock)
@patch("app.ai.agents.performance.service.emit_performance_telemetry")
@patch("app.ai.agents.performance.service.log_prompt_snapshot")
async def test_analyze_context_success(mock_snapshot, mock_telemetry, mock_analyze):
    from app.ai.agents.performance.schemas import PerformanceAnalysis, PerformanceAnalysisSchema, CostMetrics, AgentMetadata
    
    mock_analyze.return_value = PerformanceAnalysis(
        analysis=PerformanceAnalysisSchema(
            overall_score=5,
            confidence=1.0,
            analysis_summary="This is a summary of at least fifty characters long."
        ),
        cost_metrics=CostMetrics(),
        metadata=AgentMetadata(
            execution_id="123",
            agent_version="1.0",
            prompt_version="1.0",
            prompt_hash="xyz",
            model="gpt-4o",
            provider="openai"
        )
    )
    
    state = {
        "execution_id": "123",
        "context_bundle": {"data": "test"},
        "workflow_id": "wf-1"
    }
    
    result = await PerformanceAnalysisService.analyze_context(state)
    
    assert result["analysis"]["overall_score"] == 5
    mock_telemetry.assert_called_once()
    mock_snapshot.assert_called_once()
