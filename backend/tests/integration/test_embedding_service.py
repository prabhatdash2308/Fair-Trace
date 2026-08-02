import pytest
import uuid
from unittest.mock import AsyncMock, patch, MagicMock
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.ai.embeddings.service import EmbeddingService
from models.db.document_chunk import DocumentChunk
from models.enums import EmbeddingStatus, ChunkStatus
from app.ai.embeddings.models import BatchEmbeddingResponse, EmbeddingVector, TokenAccounting
from config import Settings

@pytest.fixture
def mock_db():
    db = MagicMock(spec=Session)
    return db

@pytest.fixture
def mock_settings():
    return Settings(
        database_url="sqlite:///./test.db",
        openai_api_key="test-key",
        jwt_secret_key="secret",
        qdrant_collection_name="test_collection"
    )

@pytest.fixture
def mock_vector_store():
    return AsyncMock()

@pytest.fixture
def embedding_service(mock_db, mock_settings, mock_vector_store):
    with patch("app.ai.embeddings.registry.EmbeddingProviderRegistry.get_provider") as mock_get_provider:
        mock_provider = AsyncMock()
        mock_provider.provider_name = "MockProvider"
        mock_provider.model_name = "mock-model"
        mock_provider.dimension = 1536
        mock_get_provider.return_value = mock_provider
        
        service = EmbeddingService(mock_db, mock_settings, mock_vector_store)
        service.provider = mock_provider
        return service

@pytest.mark.asyncio
async def test_embed_document_success(embedding_service, mock_db, mock_vector_store):
    doc_id = uuid.uuid4()
    chunk1_id = uuid.uuid4()
    chunk2_id = uuid.uuid4()
    
    # Mock chunks
    mock_chunks = [
        DocumentChunk(
            id=chunk1_id, document_id=doc_id, text="Chunk 1", 
            embedding_status=EmbeddingStatus.PENDING.value,
            chunk_index=0, token_estimate=10, checksum="c1", metadata_={}
        ),
        DocumentChunk(
            id=chunk2_id, document_id=doc_id, text="Chunk 2", 
            embedding_status=EmbeddingStatus.PENDING.value,
            chunk_index=1, token_estimate=15, checksum="c2", metadata_={}
        )
    ]
    
    mock_db.query().filter().order_by().all.return_value = mock_chunks
    
    # Mock provider response
    mock_response = BatchEmbeddingResponse(
        vectors=[
            EmbeddingVector(chunk_id=str(chunk1_id), vector=[0.1]*1536, token_count=10),
            EmbeddingVector(chunk_id=str(chunk2_id), vector=[0.2]*1536, token_count=15)
        ],
        accounting=TokenAccounting(total_tokens=25, prompt_tokens=25, estimated_cost_usd=0.001),
        model="mock-model",
        provider="MockProvider",
        version="1.0",
        duration_ms=100
    )
    embedding_service.provider.embed_batch.return_value = mock_response
    
    res = await embedding_service.embed_document(str(doc_id), str(uuid.uuid4()))
    
    assert res["status"] == "completed"
    assert res["chunks_total"] == 2
    assert res["chunks_embedded"] == 2
    assert res["batches"] == 1
    
    mock_vector_store.upsert_batch.assert_called_once()
    
    assert mock_chunks[0].embedding_status == EmbeddingStatus.EMBEDDED.value
    assert mock_chunks[0].embedding_provider == "MockProvider"
