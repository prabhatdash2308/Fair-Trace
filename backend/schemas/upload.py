"""
ReviewGuard AI — Upload Schemas
Strict API response definitions for document ingestion.
Never exposes internal storage details.
"""
from typing import Optional, Generic, TypeVar, Any
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

from models.enums import DocumentStatus


class DocumentResponse(BaseModel):
    """
    Publicly safe representation of a Document.
    """
    id: UUID
    filename: str = Field(..., alias="original_filename")
    type: str = Field(..., alias="mime_type")
    size: int = Field(..., alias="file_size_bytes")
    status: DocumentStatus
    uploaded_by: Optional[UUID] = None
    uploaded_at: datetime = Field(..., alias="created_at")

    class Config:
        from_attributes = True
        populate_by_name = True


T = TypeVar("T")

class BaseAPIResponse(BaseModel, Generic[T]):
    """Normalized Enterprise API Response wrapper."""
    success: bool
    data: Optional[T] = None
    message: Optional[str] = None

class ErrorDetail(BaseModel):
    code: str
    message: str

class APIErrorResponse(BaseModel):
    success: bool = False
    error: ErrorDetail
