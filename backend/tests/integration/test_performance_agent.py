import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.ai.agents.performance.agent import PerformanceAgent
from app.ai.agents.performance.exceptions import TokenLimitError
from app.ai.agents.performance.schemas import PerformanceAnalysisSchema, PerformanceAnalysis

@pytest.fixture
def mock_context_bundle():
    return {
        "employee_id": "123",
        "sections": [
            {"heading": "Strengths", "content": "Good at Python."}
        ]
    }

@pytest.mark.asyncio
async def test_agent_initialization():
    agent = PerformanceAgent()
    assert agent.model_name == "gpt-4o"
    from app.ai.core.llm_provider import OpenAIProvider
    assert isinstance(agent.provider, OpenAIProvider)
    assert agent.prompt_version == "1.0"

@pytest.mark.asyncio
async def test_analyze_success(mock_context_bundle):
    # Mock the LLM provider to avoid calling OpenAI
    agent = PerformanceAgent()
    
    mock_llm_result = {
        "parsed_data": PerformanceAnalysisSchema(
            overall_score=4,
            confidence=0.9,
            strengths=["Python"],
            improvement_areas=["None"],
            key_observations=[{"observation": "Good coding", "evidence": "Good at Python.", "impact": "High"}],
            goal_progress=[{"goal_name": "Learn Go", "status": "On Track", "notes": "Doing well"}],
            risk_flags=[],
            analysis_summary="This is a summary of at least 50 characters so it passes the business validation rule."
        ),
        "usage": {
            "prompt_tokens": 100,
            "completion_tokens": 50,
            "total_tokens": 150
        },
        "model_used": "gpt-4o"
    }
    
    with patch.object(agent, "_execute_with_retry", new_callable=AsyncMock) as mock_execute:
        mock_execute.return_value = mock_llm_result
        
        result = await agent.analyze(mock_context_bundle, execution_id="test-123")
        
        assert isinstance(result, PerformanceAnalysis)
        assert result.analysis.overall_score == 4
        assert result.cost_metrics.total_tokens == 150
        assert result.metadata.execution_id == "test-123"

@pytest.mark.asyncio
async def test_token_limit_safeguard(mock_context_bundle):
    agent = PerformanceAgent()
    
    # Mock token estimation to return a huge number
    with patch("app.ai.agents.performance.agent.estimate_tokens", return_value=150000):
        with pytest.raises(TokenLimitError):
            await agent.analyze(mock_context_bundle, execution_id="test-123")
