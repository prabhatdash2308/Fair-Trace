"""
Data models for Vector Store operations.
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class VectorMetadata(BaseModel):
    review_cycle_id: Optional[str] = None
    employee_id: Optional[str] = None
    document_type: Optional[str] = None
    chunk_id: Optional[str] = None
    source: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    correlation_id: Optional[str] = None

class VectorRecord(BaseModel):
    id: str
    vector: List[float]
    metadata: VectorMetadata
    payload: Dict[str, Any] = Field(default_factory=dict)

class VectorSearchRequest(BaseModel):
    vector: List[float]
    top_k: int = Field(default=5, gt=0)
    filter: Optional[Dict[str, Any]] = None
    score_threshold: Optional[float] = None

class SearchMatch(BaseModel):
    id: str
    score: float
    metadata: VectorMetadata
    payload: Dict[str, Any]

class VectorSearchResponse(BaseModel):
    matches: List[SearchMatch]
