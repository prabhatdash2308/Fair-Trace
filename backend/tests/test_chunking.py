import pytest
from app.ai.chunking.validator import ChunkValidator
from app.ai.chunking.exceptions import ValidationFailedError, OversizedChunkError
from app.ai.chunking.chunk_models import ChunkModel, ChunkMetadata
from app.ai.chunking.utils import estimate_tokens
from uuid import uuid4

def test_chunk_validator_success():
    chunks = [
        ChunkModel(
            document_id=uuid4(),
            chunk_index=0,
            text="Valid text",
            start_offset=0,
            end_offset=10,
            token_estimate=10,
            character_count=10,
            word_count=2,
            checksum="abc",
            metadata=ChunkMetadata(parser_version="1.0", chunker="test", chunk_version="1.0", strategy_version="1.0")
        )
    ]
    # Should not raise
    ChunkValidator.validate(chunks)

def test_chunk_validator_empty():
    chunks = [
        ChunkModel(
            document_id=uuid4(),
            chunk_index=0,
            text="   \n   ",
            start_offset=0,
            end_offset=5,
            token_estimate=0,
            character_count=5,
            word_count=0,
            checksum="abc",
            metadata=ChunkMetadata(parser_version="1.0", chunker="test", chunk_version="1.0", strategy_version="1.0")
        )
    ]
    with pytest.raises(ValidationFailedError, match="empty or whitespace only"):
        ChunkValidator.validate(chunks)

def test_chunk_validator_oversized():
    chunks = [
        ChunkModel(
            document_id=uuid4(),
            chunk_index=0,
            text="huge chunk",
            start_offset=0,
            end_offset=10,
            token_estimate=999999,
            character_count=10,
            word_count=2,
            checksum="abc",
            metadata=ChunkMetadata(parser_version="1.0", chunker="test", chunk_version="1.0", strategy_version="1.0")
        )
    ]
    with pytest.raises(OversizedChunkError):
        ChunkValidator.validate(chunks)

def test_token_estimator():
    tokens = estimate_tokens("Hello world")
    assert tokens > 0
    assert tokens == 2 # cl100k_base translates this to 2 tokens typically
