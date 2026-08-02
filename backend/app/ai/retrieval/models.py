from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid

class RetrievalQuery(BaseModel):
    query: str
    top_k: Optional[int] = None
    score_threshold: Optional[float] = None
    search_mode: Optional[str] = None
    organization_id: Optional[str] = None
    user_id: Optional[str] = None
    document_id: Optional[str] = None
    document_type: Optional[str] = None
    section: Optional[str] = None
    heading: Optional[str] = None

class RetrievedChunk(BaseModel):
    document_id: str
    chunk_id: str
    text: str
    similarity_score: float
    heading: Optional[str] = None
    section: Optional[str] = None
    document_type: Optional[str] = None
    parser_version: Optional[str] = None
    chunk_version: Optional[str] = None
    chunk_index: int = 0
    embedding_model: Optional[str] = None
    embedding_provider: Optional[str] = None
    token_count: int
    checksum: str
    vector_id: str
    
class ContextBundleStatistics(BaseModel):
    total_chunks: int = 0
    total_documents: int = 0
    total_tokens: int = 0
    build_time_ms: int = 0

class ContextBundleMetadata(BaseModel):
    headings: List[str] = Field(default_factory=list)
    sections: List[str] = Field(default_factory=list)

class ContextBundle(BaseModel):
    statistics: ContextBundleStatistics = Field(default_factory=ContextBundleStatistics)
    metadata: ContextBundleMetadata = Field(default_factory=ContextBundleMetadata)
    combined_context: str = ""
    chunks: List[RetrievedChunk] = Field(default_factory=list)

class RetrievalMetrics(BaseModel):
    retrieval_id: str
    duration_ms: int
    embedding_ms: int
    qdrant_ms: int
    ranking_ms: int
    filter_ms: int
    context_ms: int
    returned_chunks: int
    discarded_chunks: int
    duplicate_chunks: int
    tokens: int
    highest_score: float
    lowest_score: float

class RetrievalResponse(BaseModel):
    retrieval_id: str
    query_embedding_model: str
    duration_ms: int
    returned_chunks: int
    discarded_duplicates: int
    context_tokens: int
    highest_score: float
    lowest_score: float
    results: List[RetrievedChunk]
