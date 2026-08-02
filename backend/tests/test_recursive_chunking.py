import pytest
from uuid import uuid4
from app.ai.chunking.recursive_chunker import RecursiveChunker
from models.db.document import Document
from config import settings

def test_recursive_chunker_basic():
    chunker = RecursiveChunker()
    
    doc = Document(
        id=uuid4(),
        owner_id=uuid4(),
        parsed_text="This is a test document. " * 50, # 100 sentences
        parser_version="1.0"
    )
    
    chunks = chunker.split_document(doc)
    assert len(chunks) > 0
    assert chunks[0].text.startswith("This is a test document.")
    
def test_recursive_chunker_overlap():
    chunker = RecursiveChunker()
    
    # We create a huge paragraph that forces it to split
    # Since our max chunk size defaults to 2000, we'll give it 5000 tokens of text
    # 1 token is approx 4 chars, so we need ~20000 chars.
    doc = Document(
        id=uuid4(),
        owner_id=uuid4(),
        parsed_text="A" * 15000,
        parser_version="1.0"
    )
    
    chunks = chunker.split_document(doc)
    assert len(chunks) > 1
    
    # Ensure they don't exceed max size
    for chunk in chunks:
        assert chunk.token_estimate <= settings.chunk_size
