import pytest
from app.ai.retrieval.context_builder import ContextBuilder
from app.ai.retrieval.models import RetrievedChunk
from app.ai.retrieval.exceptions import InvalidPayloadError
import uuid

def mock_chunk(token_count: int, checksum: str, chunk_id: str = None, vector_id: str = None, heading: str = "") -> RetrievedChunk:
    return RetrievedChunk(
        document_id="d1",
        chunk_id=chunk_id or str(uuid.uuid4()),
        text="Sample text",
        similarity_score=0.9,
        heading=heading,
        section="",
        chunk_index=0,
        vector_id=vector_id or str(uuid.uuid4()),
        embedding_model="test-model",
        token_count=token_count,
        checksum=checksum
    )

def test_duplicate_injection():
    builder = ContextBuilder(max_context_tokens=1000)
    
    shared_checksum = "hash123"
    shared_chunk_id = "chunk_a"
    shared_vector_id = "vec_a"
    
    chunks = [
        mock_chunk(100, shared_checksum, shared_chunk_id, shared_vector_id),
        mock_chunk(100, shared_checksum, shared_chunk_id, shared_vector_id), # Duplicate
        mock_chunk(100, shared_checksum, shared_chunk_id, shared_vector_id)  # Duplicate
    ]
    
    bundle = builder.build(chunks)
    
    # Verify only one survives
    assert len(bundle.chunks) == 1
    assert bundle.statistics.total_tokens == 100

def test_token_limit_cutoff():
    builder = ContextBuilder(max_context_tokens=250)
    
    chunks = [
        mock_chunk(100, "hash1"),
        mock_chunk(100, "hash2"),
        mock_chunk(100, "hash3") # Should be rejected, would make total 300 > 250
    ]
    
    bundle = builder.build(chunks)
    
    assert len(bundle.chunks) == 2
    assert bundle.statistics.total_tokens == 200

def test_invalid_payload_rejected():
    builder = ContextBuilder(max_context_tokens=1000)
    
    # Missing checksum
    bad_chunk = mock_chunk(100, "")
    bad_chunk.checksum = None
    
    with pytest.raises(InvalidPayloadError):
        builder.build([bad_chunk])

def test_metadata_aggregation():
    builder = ContextBuilder(max_context_tokens=1000)
    
    chunks = [
        mock_chunk(100, "hash1", heading="Summary"),
        mock_chunk(100, "hash2", heading="Experience"),
        mock_chunk(100, "hash3", heading="Summary") # Duplicate heading
    ]
    
    bundle = builder.build(chunks)
    
    assert len(bundle.metadata.headings) == 2
    assert "Summary" in bundle.metadata.headings
    assert "Experience" in bundle.metadata.headings
