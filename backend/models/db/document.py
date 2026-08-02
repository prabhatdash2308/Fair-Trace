from uuid import uuid4
from sqlalchemy import Column, String, Integer, Enum, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID

from models.db.base import Base, TimestampMixin
from models.enums import DocumentStatus, ParsingStatus


class Document(Base, TimestampMixin):
    """
    Enterprise Document storage tracking.
    Never exposes internal storage_key to the client.
    """
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Client-facing metadata
    original_filename = Column(String, nullable=False)
    mime_type = Column(String, nullable=False)
    extension = Column(String, nullable=False)
    file_size_bytes = Column(Integer, nullable=False)
    
    # Internal Storage Info
    storage_provider = Column(String, nullable=False, default="local")
    storage_key = Column(String, nullable=False, unique=True)
    
    # Hash for duplicate detection and integrity
    checksum = Column(String, nullable=False, index=True)
    
    # Ownership (Document can belong to a user and org)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    organization_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    # Lifecycle
    status = Column(Enum(DocumentStatus), nullable=False, default=DocumentStatus.UPLOADING, index=True)
    virus_scan_status = Column(String, nullable=True)
    processing_error = Column(String, nullable=True)

    # ── Parsing Metadata ───────────────────────────────────────────────────────
    parsed_text = Column(String, nullable=True)
    page_count = Column(Integer, nullable=False, default=0)
    word_count = Column(Integer, nullable=False, default=0)
    character_count = Column(Integer, nullable=False, default=0)
    parser_used = Column(String, nullable=True)
    parser_version = Column(String, nullable=True)
    parse_duration_ms = Column(Integer, nullable=True)
    parsing_status = Column(Enum(ParsingStatus), nullable=False, default=ParsingStatus.PENDING, index=True)
    parsed_at = Column(DateTime, nullable=True)
    parsing_error = Column(String, nullable=True)
