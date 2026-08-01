"""
Data models for Embedding requests, chunks, and responses.
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Union, Optional

class Chunk(BaseModel):
    text: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class EmbeddingRequest(BaseModel):
    text: Union[str, List[str]]
    model: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class EmbeddingVector(BaseModel):
    vector: List[float]
    text: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ProviderResponse(BaseModel):
    vectors: List[List[float]]
    total_tokens: int

class EmbeddingResponse(BaseModel):
    vectors: List[EmbeddingVector]
    model_used: str
    total_tokens: int = Field(default=0, ge=0)
    cost: float = Field(default=0.0, ge=0.0)
