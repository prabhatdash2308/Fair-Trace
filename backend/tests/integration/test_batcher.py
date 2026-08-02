import pytest
from app.ai.embeddings.batcher import Batcher
from app.ai.embeddings.models import ChunkToEmbed
from app.ai.embeddings.exceptions import InvalidInputError

def test_batcher_splits_correctly():
    chunks = [ChunkToEmbed(chunk_id=str(i), text=f"Text {i}") for i in range(10)]
    
    batches = Batcher.validate_and_batch(chunks, batch_size=3)
    
    assert len(batches) == 4
    assert len(batches[0]) == 3
    assert len(batches[3]) == 1

def test_batcher_rejects_empty():
    with pytest.raises(InvalidInputError):
        Batcher.validate_and_batch([], batch_size=3)

def test_batcher_rejects_empty_chunk():
    chunks = [
        ChunkToEmbed(chunk_id="1", text="Valid"),
        ChunkToEmbed(chunk_id="2", text="   "),
    ]
    with pytest.raises(InvalidInputError, match="whitespace"):
        Batcher.validate_and_batch(chunks, batch_size=3)

def test_batcher_rejects_duplicate_ids():
    chunks = [
        ChunkToEmbed(chunk_id="1", text="Valid"),
        ChunkToEmbed(chunk_id="1", text="Duplicate ID"),
    ]
    with pytest.raises(InvalidInputError, match="Duplicate chunk ID"):
        Batcher.validate_and_batch(chunks, batch_size=3)

def test_batcher_token_limit():
    chunks = [ChunkToEmbed(chunk_id="1", text="Long text")]
    
    def fake_estimator(text: str) -> int:
        return 9000
        
    with pytest.raises(InvalidInputError, match="exceeds token limit"):
        Batcher.validate_and_batch(chunks, batch_size=3, token_estimator=fake_estimator)
