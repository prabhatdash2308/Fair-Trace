import pytest
from unittest.mock import AsyncMock, patch
from app.ai.agents.bias.agent import BiasAgent
from app.ai.agents.bias.exceptions import TokenLimitError
from app.ai.agents.bias.schemas import BiasAnalysisSchema, BiasAnalysis
from app.ai.agents.bias.enums import BiasSeverity, RiskLevel
from app.ai.agents.bias.taxonomy import BiasType

@pytest.fixture
def mock_context():
    return {"data": "test_context"}

@pytest.fixture
def mock_performance():
    return {"overall_score": 4}

@pytest.mark.asyncio
async def test_bias_agent_initialization():
    agent = BiasAgent()
    assert agent.model_name == "gpt-4o"
    from app.ai.core.llm_provider import OpenAIProvider
    assert isinstance(agent.provider, OpenAIProvider)
    assert agent.prompt_version == "1.0"

@pytest.mark.asyncio
async def test_bias_analyze_success(mock_context, mock_performance):
    agent = BiasAgent()
    
    mock_llm_result = {
        "parsed_data": BiasAnalysisSchema(
            overall_bias_score=0.2,
            risk_level=RiskLevel.LOW,
            detected_biases=[
                {
                    "category": BiasType.RECENCY,
                    "severity": BiasSeverity.LOW,
                    "confidence": 0.9,
                    "evidence": ["Recent good performance"],
                    "evidence_ids": ["chunk_1"],
                    "recommendation": "Review older feedback"
                }
            ],
            unsupported_claims=[],
            missing_evidence=[],
            fairness_assessment="Fair review",
            confidence=0.95,
            summary="Good"
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
        
        result = await agent.analyze(mock_context, mock_performance, execution_id="test-123")
        
        assert isinstance(result, BiasAnalysis)
        assert result.analysis.overall_bias_score == 0.2
        assert len(result.analysis.detected_biases) == 1
        assert result.cost_metrics.total_tokens == 150
        assert result.metadata.execution_id == "test-123"

@pytest.mark.asyncio
async def test_bias_token_limit_safeguard(mock_context, mock_performance):
    agent = BiasAgent()
    
    with patch("app.ai.agents.bias.agent.estimate_tokens", return_value=150000):
        with pytest.raises(TokenLimitError):
            await agent.analyze(mock_context, mock_performance, execution_id="test-123")
