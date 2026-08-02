import pytest
import time
from unittest.mock import AsyncMock, patch, MagicMock
from app.ai.retrieval.service import SemanticRetriever
from app.ai.retrieval.models import RetrievalQuery
from config import Settings
import uuid

@pytest.fixture
def mock_settings():
    settings = Settings()
    settings.retrieval_top_k = 10
    settings.retrieval_score_threshold = 0.7
    settings.max_context_tokens = 12000
    return settings

class MockVectorPoint:
    def __init__(self, score: float, payload: dict):
        self.score = score
        self.payload = payload
        self.id = str(uuid.uuid4())

@pytest.mark.asyncio
async def test_large_corpus_retrieval(mock_settings):
    """
    Simulates retrieving from a massive index.
    The VectorStore returns Top K quickly, the service processes it.
    """
    
    # 1. Mock Vector Store
    mock_vector_store = AsyncMock()
    
    # Generate 25 top chunks from a "10,000 chunk" simulated vector search
    mock_results = []
    for i in range(25):
        mock_results.append(MockVectorPoint(
            score=0.9 - (i * 0.01),
            payload={
                "document_id": "d1",
                "chunk_id": f"chunk_{i}",
                "text": f"Chunk text {i}",
                "checksum": f"hash_{i}",
                "embedding_model": "test-model",
                "token_count": 500
            }
        ))
    mock_vector_store.search.return_value = mock_results
    
    # 2. Mock Embedding Provider Registry
    mock_provider = AsyncMock()
    mock_provider.model_name = "test-model"
    mock_provider.embed_batch.return_value = MagicMock(
        vectors=[MagicMock(vector=[0.1]*1536)]
    )
    
    with patch("app.ai.retrieval.service.EmbeddingProviderRegistry.get_provider", return_value=mock_provider):
        service = SemanticRetriever(settings=mock_settings, vector_store=mock_vector_store)
        
        query = RetrievalQuery(query="large corpus test", search_mode="EXHAUSTIVE")
        
        start_time = time.time()
        response = await service.search(query)
        duration_ms = int((time.time() - start_time) * 1000)
        
        assert response.returned_chunks == 24 # 12000 token limit / 500 = 24 max context
        assert response.context_tokens == 12000
        assert duration_ms < 500 # Should be basically 0ms locally
