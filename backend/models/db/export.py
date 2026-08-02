import uuid
import datetime
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum, ForeignKey, JSON, Integer
from sqlalchemy.orm import relationship
from models.db.base import Base
from enum import Enum

class ExportStatus(str, Enum):
    PENDING = "PENDING"
    GENERATING = "GENERATING"
    READY = "READY"
    FAILED = "FAILED"
    EXPIRED = "EXPIRED"

class ExportFormat(str, Enum):
    PDF = "PDF"
    HTML = "HTML"
    JSON = "JSON"

class ReportExport(Base):
    __tablename__ = "report_exports"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    workflow_id = Column(String(100), nullable=False, index=True)
    report_id = Column(String(100), nullable=False)
    version = Column(String(50), nullable=False, default="1.0")
    
    format = Column(SQLEnum(ExportFormat), default=ExportFormat.PDF, nullable=False)
    status = Column(SQLEnum(ExportStatus), default=ExportStatus.PENDING, nullable=False)
    
    checksum = Column(String(256), nullable=True)
    storage_path = Column(String(500), nullable=True)
    
    generated_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    generated_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    
    download_count = Column(Integer, default=0)
    file_size_bytes = Column(Integer, nullable=True)
    signature = Column(String(1024), nullable=True)
    metadata_ = Column("metadata", JSON, default=dict)
