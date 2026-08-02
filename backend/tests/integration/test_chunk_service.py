import pytest
from uuid import uuid4
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.ai.chunking.chunk_service import ChunkService
from models.db.document import Document
from models.db.document_chunk import DocumentChunk
from models.enums import ChunkStrategy, ParsingStatus
from app.ai.chunking.sentence_chunker import SentenceChunker
from app.ai.chunking.recursive_chunker import RecursiveChunker
from app.ai.chunking.semantic_chunker import SemanticChunker

def test_chunk_service_unparsed_doc_fails(test_db: Session):
    doc_id = uuid4()
    user_id = uuid4()
    
    doc = Document(
        id=doc_id,
        owner_id=user_id,
        original_filename="test.pdf",
        extension=".pdf",
        storage_key=f"abc-{doc_id}",
        mime_type="application/pdf",
        file_size_bytes=100,
        checksum="123",
        parsing_status=ParsingStatus.PENDING # Not parsed!
    )
    test_db.add(doc)
    test_db.commit()
    
    service = ChunkService(test_db)
    with pytest.raises(HTTPException, match="not in PARSED state"):
        service.chunk_document(doc_id, user_id)

def test_chunk_service_success(test_db: Session):
    doc_id = uuid4()
    user_id = uuid4()
    
    doc = Document(
        id=doc_id,
        owner_id=user_id,
        original_filename="test.pdf",
        extension=".pdf",
        storage_key=f"abc-{doc_id}",
        mime_type="application/pdf",
        file_size_bytes=100,
        checksum="123",
        parsing_status=ParsingStatus.PARSED,
        parsed_text="This is a fully parsed document ready for chunking.",
        parser_version="1.0"
    )
    test_db.add(doc)
    test_db.commit()
    
    service = ChunkService(test_db)
    stats = service.chunk_document(doc_id, user_id, ChunkStrategy.SENTENCE)
    
    assert stats.chunk_count > 0
    assert stats.status == "completed"
    
    # Verify DB insertion
    db_chunks = test_db.query(DocumentChunk).filter(DocumentChunk.document_id == doc_id).all()
    assert len(db_chunks) == stats.chunk_count
    
def test_chunk_service_duplicate_rejection(test_db: Session):
    doc_id = uuid4()
    user_id = uuid4()
    
    doc = Document(
        id=doc_id,
        owner_id=user_id,
        original_filename="test.pdf",
        extension=".pdf",
        storage_key=f"abc-{doc_id}",
        mime_type="application/pdf",
        file_size_bytes=100,
        checksum="123",
        parsing_status=ParsingStatus.PARSED,
        parsed_text="Just one sentence.",
        parser_version="1.0"
    )
    test_db.add(doc)
    test_db.commit()
    
    service = ChunkService(test_db)
    
    # First run
    stats1 = service.chunk_document(doc_id, user_id, ChunkStrategy.SENTENCE)
    assert stats1.chunk_count > 0
    assert stats1.duplicates_removed == 0
    
    # Second run should trigger duplicate rejection via checksum unique constraint
    stats2 = service.chunk_document(doc_id, user_id, ChunkStrategy.SENTENCE)
    assert stats2.chunk_count == 0
    assert stats2.duplicates_removed > 0
