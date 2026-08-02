from sqlalchemy import Column, String, Integer, Float, ForeignKey, JSON, Index, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime, timezone

from models.db.base import Base
from models.enums import ChunkStrategy, ChunkStatus

class DocumentChunk(Base):
    """
    Represents a chunk of text extracted from a parsed document,
    ready for embedding or LLM ingestion.
    """
    __tablename__ = "document_chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    
    # Ordering and Position
    chunk_index = Column(Integer, nullable=False)
    start_offset = Column(Integer, nullable=False)
    end_offset = Column(Integer, nullable=False)
    page_start = Column(Integer, nullable=True)
    page_end = Column(Integer, nullable=True)
    
    # Content
    text = Column(Text, nullable=False)
    
    # Statistics
    token_estimate = Column(Integer, nullable=False)
    character_count = Column(Integer, nullable=False)
    word_count = Column(Integer, nullable=False)
    
    # Uniqueness & Strategy
    checksum = Column(String, nullable=False) # sha256(document_id + chunk_index + text)
    strategy = Column(String, nullable=False, default=ChunkStrategy.RECURSIVE.value)
    
    # AI Pipeline Metadata (populated in 11.4)
    semantic_confidence = Column(Float, nullable=True)
    status = Column(String, nullable=False, default=ChunkStatus.PENDING.value)
    embedding_status = Column(String, nullable=True)
    vector_id = Column(String, nullable=True)
    embedding_model = Column(String, nullable=True)
    embedding_provider = Column(String, nullable=True)
    embedding_version = Column(String, nullable=True)
    embedding_dimensions = Column(Integer, nullable=True)
    embedding_created_at = Column(DateTime(timezone=True), nullable=True)
    embedding_duration_ms = Column(Integer, nullable=True)
    embedding_checksum = Column(String, nullable=True)
    token_count = Column(Integer, nullable=True)
    embedding_error = Column(String, nullable=True)
    
    # Flexible metadata (headings, versioning, HR context)
    # Using JSON to support SQLite in tests, but in Postgres this is JSONB
    metadata_ = Column("metadata", JSON().with_variant(JSONB, "postgresql"), nullable=False, default=dict)

    # Relationships
    document = relationship("Document", backref="chunks")

    __table_args__ = (
        Index("ix_document_chunks_document_id", "document_id"),
        Index("ix_document_chunks_chunk_index", "document_id", "chunk_index"),
        Index("ix_document_chunks_checksum", "checksum", unique=True),
        Index("ix_document_chunks_status", "status"),
    )

    def __repr__(self) -> str:
        return f"<DocumentChunk {self.id} doc={self.document_id} idx={self.chunk_index} stat={self.status}>"
