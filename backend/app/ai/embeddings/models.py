from typing import List
from pydantic import BaseModel, Field

class ChunkToEmbed(BaseModel):
    chunk_id: str
    text: str

class EmbeddingVector(BaseModel):
    chunk_id: str
    vector: List[float]
    token_count: int

class TokenAccounting(BaseModel):
    total_tokens: int
    prompt_tokens: int
    estimated_cost_usd: float

class BatchEmbeddingResponse(BaseModel):
    vectors: List[EmbeddingVector]
    accounting: TokenAccounting
    model: str
    provider: str
    version: str
    duration_ms: int
