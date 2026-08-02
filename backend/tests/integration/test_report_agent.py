import pytest
from unittest.mock import AsyncMock, patch
from app.ai.agents.report.agent import ReportGenerationAgent
from app.ai.agents.report.exceptions import TokenLimitError
from app.ai.agents.report.schemas import (
    EnterprisePerformanceReportSchema, 
    EnterprisePerformanceReport,
    DevelopmentPlan,
    RiskSummary,
    Recommendation,
    Priority
)

@pytest.fixture
def mock_context(): return {"data": "test"}

@pytest.fixture
def mock_performance(): return {"analysis": {"overall_score_confidence": 0.95}}

@pytest.fixture
def mock_bias(): return {"bias_analysis": {"detected_biases": []}}

@pytest.fixture
def mock_explainability(): return {"analysis": {"transparency_metrics": {"coverage": 1.0}, "evidence_map": ["1", "2"]}}

@pytest.mark.asyncio
async def test_report_agent_initialization():
    agent = ReportGenerationAgent()
    assert agent.model_name == "gpt-4o"
    from app.ai.core.llm_provider import OpenAIProvider
    assert isinstance(agent.provider, OpenAIProvider)
    assert agent.prompt_version == "1.0"

@pytest.mark.asyncio
async def test_report_generate_success(mock_context, mock_performance, mock_bias, mock_explainability):
    agent = ReportGenerationAgent()
    
    mock_llm_result = {
        "parsed_data": EnterprisePerformanceReportSchema(
            employee_summary={},
            executive_summary="Excellent.",
            overall_rating=4.5,
            overall_confidence=0.9,
            performance_highlights=[],
            strengths=[],
            improvement_areas=[],
            goal_progress=[],
            development_plan=DevelopmentPlan(plan_90_day="do this"),
            recommended_actions=[Recommendation(title="T", recommendation="R", priority=Priority.HIGH, impact="I", effort="E", confidence=1.0)],
            risk_summary=RiskSummary(overall_risk="low", bias_risk="low", confidence_risk="low", missing_evidence=0, unsupported_claims=0),
            manager_notes="Good job."
        ),
        "usage": {"prompt_tokens": 200, "completion_tokens": 150, "total_tokens": 350},
        "model_used": "gpt-4o"
    }
    
    with patch.object(agent, "_execute_with_retry", new_callable=AsyncMock) as mock_execute:
        mock_execute.return_value = mock_llm_result
        
        result = await agent.generate(mock_context, mock_performance, mock_bias, mock_explainability, execution_id="test-123")
        
        assert "report" in result
        assert result["report"]["overall_rating"] == 4.5
        assert result["pipeline_metrics"]["total_tokens"] == 350
        assert result["metadata"]["execution_id"] == "test-123"

@pytest.mark.asyncio
async def test_report_token_limit_safeguard(mock_context, mock_performance, mock_bias, mock_explainability):
    agent = ReportGenerationAgent()
    
    with patch("app.ai.agents.report.agent.estimate_tokens", return_value=150000):
        with pytest.raises(TokenLimitError):
            await agent.generate(mock_context, mock_performance, mock_bias, mock_explainability, execution_id="test-123")
