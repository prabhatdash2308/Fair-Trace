"""
Configuration models for the Vector Store Service.
"""
from pydantic import BaseModel, Field

class VectorStoreConfig(BaseModel):
    collection_name: str = "reviewguard_default"
    vector_size: int = Field(default=1536, gt=0)
    distance_metric: str = "Cosine"
    request_timeout_seconds: float = 30.0
