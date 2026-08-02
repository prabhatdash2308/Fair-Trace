import pytest
import openai
from unittest.mock import AsyncMock, patch, MagicMock
from app.ai.embeddings.openai_service import OpenAIEmbeddingProvider
from app.ai.embeddings.models import ChunkToEmbed
from app.ai.embeddings.exceptions import RateLimitExceededError, ProviderAuthenticationError
from config import Settings

@pytest.fixture
def settings():
    return Settings(
        database_url="sqlite:///./test.db",
        openai_api_key="test-key",
        jwt_secret_key="secret"
    )

@pytest.fixture
def provider(settings):
    return OpenAIEmbeddingProvider(settings)

@pytest.mark.asyncio
@patch("app.ai.embeddings.openai_service.AsyncOpenAI")
async def test_embed_batch_success(mock_openai_class, provider):
    mock_client = AsyncMock()
    mock_openai_class.return_value = mock_client
    provider.client = mock_client
    
    mock_response = MagicMock()
    mock_response.data = [MagicMock(embedding=[0.1]*1536), MagicMock(embedding=[0.2]*1536)]
    mock_response.usage.total_tokens = 100
    mock_response.usage.prompt_tokens = 100
    mock_client.embeddings.create.return_value = mock_response
    
    chunks = [
        ChunkToEmbed(chunk_id="1", text="Hello"),
        ChunkToEmbed(chunk_id="2", text="World")
    ]
    
    res = await provider.embed_batch(chunks)
    
    assert len(res.vectors) == 2
    assert res.vectors[0].vector == [0.1]*1536
    assert res.accounting.total_tokens == 100
    assert res.model == "text-embedding-3-small"

@pytest.mark.asyncio
@patch("app.ai.embeddings.openai_service.AsyncOpenAI")
async def test_embed_batch_rate_limit_retry(mock_openai_class, provider):
    mock_client = AsyncMock()
    mock_openai_class.return_value = mock_client
    provider.client = mock_client
    
    # Fail twice, succeed on third
    mock_response = MagicMock()
    mock_response.data = [MagicMock(embedding=[0.1]*1536)]
    mock_response.usage.total_tokens = 50
    mock_response.usage.prompt_tokens = 50
    
    err_response = MagicMock()
    err_response.status_code = 429
    
    mock_client.embeddings.create.side_effect = [
        openai.RateLimitError("Rate limit", response=err_response, body={}),
        openai.RateLimitError("Rate limit", response=err_response, body={}),
        mock_response
    ]
    
    # We need to temporarily reduce the tenacity wait for tests
    # We will just verify it passes (retries internally)
    res = await provider.embed_batch([ChunkToEmbed(chunk_id="1", text="test")])
    assert len(res.vectors) == 1
    assert mock_client.embeddings.create.call_count == 3
