import pytest
from unittest.mock import AsyncMock, patch
from app.ai.agents.report.service import ReportGenerationService

@pytest.mark.asyncio
async def test_report_analyze_context_missing_fields():
    with pytest.raises(ValueError, match="Execution ID is missing"):
        await ReportGenerationService.generate_report({"context_bundle": {}})

@pytest.mark.asyncio
@patch("app.ai.agents.report.service.ReportGenerationAgent.generate", new_callable=AsyncMock)
@patch("app.ai.agents.report.service.emit_report_telemetry")
@patch("app.ai.agents.report.service.log_prompt_snapshot")
async def test_report_analyze_context_success(mock_snapshot, mock_telemetry, mock_generate):
    mock_generate.return_value = {
        "report": {},
        "pipeline_metrics": {
            "report_length": 100, "recommendation_count": 1, "strength_count": 1, 
            "improvement_count": 1, "risk_count": 1, "evidence_count": 1, 
            "overall_score": 4.5, "confidence": 0.9
        },
        "cost_metrics": {},
        "metadata": {}
    }
    
    state = {
        "execution_id": "123",
        "context_bundle": {"data": "test"},
        "performance_analysis": {"data": "test2"},
        "bias_analysis": {"data": "test3"},
        "explainability_analysis": {"data": "test4"},
        "workflow_id": "wf-1"
    }
    
    result = await ReportGenerationService.generate_report(state)
    
    assert result["pipeline_metrics"]["overall_score"] == 4.5
    mock_telemetry.assert_called_once()
    mock_snapshot.assert_called_once()
