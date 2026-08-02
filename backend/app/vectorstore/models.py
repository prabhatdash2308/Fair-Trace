from typing import List, Any, Optional
from pydantic import BaseModel, Field

class VectorPayload(BaseModel):
    """The strict metadata schema persisted in Qdrant."""
    document_id: str
    chunk_id: str
    organization_id: Optional[str] = None
    user_id: str
    heading: Optional[str] = None
    section: Optional[str] = None
    document_type: Optional[str] = None
    parser_version: Optional[str] = None
    chunk_version: Optional[str] = None
    embedding_model: str
    embedding_provider: str
    checksum: str
    created_at: str
    token_count: int

class VectorPoint(BaseModel):
    id: str  # Must be a UUID (e.g. chunk_id)
    vector: List[float]
    payload: dict
