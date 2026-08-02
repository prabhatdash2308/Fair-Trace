import pytest
from unittest.mock import AsyncMock, patch
from app.ai.agents.explainability.agent import ExplainabilityAgent
from app.ai.agents.explainability.exceptions import TokenLimitError
from app.ai.agents.explainability.schemas import (
    ExplainabilityAnalysisSchema, 
    ExplainabilityAnalysis,
    ConfidenceBreakdown,
    TransparencyMetrics
)

@pytest.fixture
def mock_context(): return {"data": "test"}

@pytest.fixture
def mock_performance(): return {"score": 4}

@pytest.fixture
def mock_bias(): return {"bias": 0.1}

@pytest.mark.asyncio
async def test_explainability_agent_initialization():
    agent = ExplainabilityAgent()
    assert agent.model_name == "gpt-4o"
    from app.ai.core.llm_provider import OpenAIProvider
    assert isinstance(agent.provider, OpenAIProvider)
    assert agent.prompt_version == "1.0"

@pytest.mark.asyncio
async def test_explainability_analyze_success(mock_context, mock_performance, mock_bias):
    agent = ExplainabilityAgent()
    
    mock_llm_result = {
        "parsed_data": ExplainabilityAnalysisSchema(
            overall_confidence=0.9,
            confidence_breakdown=ConfidenceBreakdown(performance=0.9, bias=0.9, reasoning=0.9, overall=0.9),
            reasoning_trace=[],
            decision_graph=[],
            evidence_map=[],
            transparency_metrics=TransparencyMetrics(
                coverage=1.0, evidence_density=1.0, evidence_consistency=1.0, 
                unsupported_claims_count=0, bias_adjustments_count=0, reasoning_completeness=1.0
            ),
            unsupported_claims=[],
            audit_summary="ok"
        ),
        "usage": {"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150},
        "model_used": "gpt-4o"
    }
    
    with patch.object(agent, "_execute_with_retry", new_callable=AsyncMock) as mock_execute:
        mock_execute.return_value = mock_llm_result
        
        result = await agent.analyze(mock_context, mock_performance, mock_bias, execution_id="test-123")
        
        assert isinstance(result, ExplainabilityAnalysis)
        assert result.analysis.overall_confidence == 0.9
        assert result.cost_metrics.total_tokens == 150
        assert result.metadata.execution_id == "test-123"

@pytest.mark.asyncio
async def test_explainability_token_limit_safeguard(mock_context, mock_performance, mock_bias):
    agent = ExplainabilityAgent()
    
    with patch("app.ai.agents.explainability.agent.estimate_tokens", return_value=150000):
        with pytest.raises(TokenLimitError):
            await agent.analyze(mock_context, mock_performance, mock_bias, execution_id="test-123")
