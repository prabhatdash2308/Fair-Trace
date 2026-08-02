from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from uuid import UUID
from datetime import datetime

class ChunkMetadata(BaseModel):
    parser_version: str
    chunker: str
    chunk_version: str
    strategy_version: str
    document_type: Optional[str] = None
    
    # HR-aware Metadata
    section: Optional[str] = None
    heading: Optional[str] = None
    employee_name: Optional[str] = None
    review_period: Optional[str] = None
    manager_name: Optional[str] = None
    department: Optional[str] = None
    
    class Config:
        extra = "allow" # Allow dynamic fields if needed

class ChunkModel(BaseModel):
    document_id: UUID
    chunk_index: int
    text: str
    start_offset: int
    end_offset: int
    token_estimate: int
    character_count: int
    word_count: int
    page_start: Optional[int] = None
    page_end: Optional[int] = None
    checksum: str
    semantic_confidence: float = 0.0
    metadata: ChunkMetadata

class ChunkStatistics(BaseModel):
    status: str
    strategy: str
    chunk_count: int = 0
    duplicates_removed: int = 0
    average_tokens: int = 0
    average_words: int = 0
    average_chars: int = 0
    largest_chunk: int = 0
    smallest_chunk: int = 0
    processing_ms: int = 0
    document_id: UUID
    compression_ratio: float = 1.0
