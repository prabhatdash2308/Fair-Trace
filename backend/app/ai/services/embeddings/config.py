"""
Configuration models for the Embedding Service.
"""
from pydantic import BaseModel, Field

class EmbeddingConfig(BaseModel):
    default_model: str = "text-embedding-3-small"
    chunk_size: int = Field(default=1000, gt=0)
    chunk_overlap: int = Field(default=200, ge=0)
    max_batch_size: int = Field(default=100, gt=0)
    max_retries: int = 3
