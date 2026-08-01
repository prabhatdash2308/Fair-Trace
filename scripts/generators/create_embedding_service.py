import os
from pathlib import Path

emb_dir = Path("backend/app/ai/services/embeddings")
emb_dir.mkdir(parents=True, exist_ok=True)

# 1. exceptions.py
(emb_dir / "exceptions.py").write_text('''"""
Custom exceptions for the Enterprise Embedding Service.
"""

class EmbeddingException(Exception):
    """Base exception for all Embedding service errors."""
    pass

class EmbeddingProviderError(EmbeddingException):
    """Raised when the underlying embedding provider fails."""
    pass

class ChunkingError(EmbeddingException):
    """Raised when text chunking fails (e.g., invalid parameters)."""
    pass

class EmbeddingCacheError(EmbeddingException):
    """Raised when cache operations fail."""
    pass
''', encoding="utf-8")

# 2. config.py
(emb_dir / "config.py").write_text('''"""
Configuration models for the Embedding Service.
"""
from pydantic import BaseModel, Field

class EmbeddingConfig(BaseModel):
    default_model: str = "text-embedding-3-small"
    chunk_size: int = Field(default=1000, gt=0)
    chunk_overlap: int = Field(default=200, ge=0)
    max_batch_size: int = Field(default=100, gt=0)
    max_retries: int = 3
''', encoding="utf-8")

# 3. models.py
(emb_dir / "models.py").write_text('''"""
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
''', encoding="utf-8")

# 4. chunker.py
(emb_dir / "chunker.py").write_text('''"""
Text chunking mechanism for large documents.
"""
from typing import List, Dict, Any
from .models import Chunk
from .exceptions import ChunkingError

class Chunker:
    @staticmethod
    def chunk_text(text: str, chunk_size: int, chunk_overlap: int, metadata: Dict[str, Any] = None) -> List[Chunk]:
        """
        Splits text into overlapping chunks.
        In production, use LangChain's RecursiveCharacterTextSplitter.
        """
        if chunk_size <= chunk_overlap:
            raise ChunkingError("chunk_size must be greater than chunk_overlap")
            
        if not text:
            return []
            
        meta = metadata or {}
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = min(start + chunk_size, text_length)
            chunk_text = text[start:end]
            chunks.append(Chunk(text=chunk_text, metadata=meta))
            if end == text_length:
                break
            start += chunk_size - chunk_overlap
            
        return chunks
''', encoding="utf-8")

# 5. cache.py
(emb_dir / "cache.py").write_text('''"""
Caching for embeddings to save cost and latency.
"""
import hashlib
from typing import Optional, List

class EmbeddingCache:
    def __init__(self):
        self._cache = {}
        
    def _hash(self, text: str, model: str) -> str:
        return hashlib.sha256(f"{model}:{text}".encode('utf-8')).hexdigest()
        
    def get(self, text: str, model: str) -> Optional[List[float]]:
        return self._cache.get(self._hash(text, model))
        
    def set(self, text: str, model: str, vector: List[float]) -> None:
        self._cache[self._hash(text, model)] = vector
''', encoding="utf-8")

# 6. telemetry.py
(emb_dir / "telemetry.py").write_text('''"""
Telemetry tracking for Embedding Service.
"""
import logging

logger = logging.getLogger(__name__)

class Telemetry:
    def __init__(self):
        self.total_requests = 0
        self.total_chunks = 0
        self.total_cost = 0.0
        
    def record_embedding(self, correlation_id: str, model: str, latency_ms: int, chunks: int, cost: float) -> None:
        self.total_requests += 1
        self.total_chunks += chunks
        self.total_cost += cost
        logger.info(f"[EmbeddingTelemetry {correlation_id}] Model: {model} | Latency: {latency_ms}ms | Chunks: {chunks} | Cost: ")
''', encoding="utf-8")

# 7. providers.py
(emb_dir / "providers.py").write_text('''"""
Abstract provider interface and implementations.
"""
from abc import ABC, abstractmethod
from typing import List
from .models import ProviderResponse
from .exceptions import EmbeddingProviderError

class EmbeddingProvider(ABC):
    @abstractmethod
    def embed(self, texts: List[str], model: str) -> ProviderResponse:
        pass

class OpenAIEmbeddingProvider(EmbeddingProvider):
    def __init__(self, api_key: str = "dummy"):
        self.api_key = api_key
        
    def embed(self, texts: List[str], model: str) -> ProviderResponse:
        # Dummy implementation
        try:
            vectors = []
            for t in texts:
                # generate a dummy vector of 3 dimensions for tests
                vectors.append([0.1, 0.2, 0.3])
            
            # Dummy token math: roughly length of texts // 4
            tokens = sum(len(t) // 4 for t in texts)
            return ProviderResponse(vectors=vectors, total_tokens=tokens)
        except Exception as e:
            raise EmbeddingProviderError(f"Provider failed: {str(e)}") from e
''', encoding="utf-8")

# 8. embedding_service.py
(emb_dir / "embedding_service.py").write_text('''"""
The orchestrator of the Enterprise Embedding Service.
"""
import time
from typing import List
from .config import EmbeddingConfig
from .models import EmbeddingRequest, EmbeddingResponse, EmbeddingVector, Chunk
from .providers import EmbeddingProvider
from .chunker import Chunker
from .cache import EmbeddingCache
from .telemetry import Telemetry

class EmbeddingService:
    """
    Enterprise Embedding Gateway.
    No agent should bypass this service to embed text.
    """
    def __init__(
        self,
        provider: EmbeddingProvider,
        config: EmbeddingConfig,
        cache: EmbeddingCache,
        telemetry: Telemetry
    ):
        self.provider = provider
        self.config = config
        self.cache = cache
        self.telemetry = telemetry
        # Cost per 1k tokens for text-embedding-3-small
        self.cost_per_1k = 0.00002
        
    def _calculate_cost(self, tokens: int) -> float:
        return (tokens / 1000.0) * self.cost_per_1k
        
    def embed(self, request: EmbeddingRequest, correlation_id: str) -> EmbeddingResponse:
        """
        Chunks text, checks cache, and executes embedding for missing chunks via batch.
        """
        start_time = time.perf_counter()
        model = request.model or self.config.default_model
        
        # Normalize to list
        texts_to_process = [request.text] if isinstance(request.text, str) else request.text
        
        # 1. Chunking
        all_chunks: List[Chunk] = []
        for text in texts_to_process:
            chunks = Chunker.chunk_text(
                text=text,
                chunk_size=self.config.chunk_size,
                chunk_overlap=self.config.chunk_overlap,
                metadata=request.metadata
            )
            all_chunks.extend(chunks)
            
        # 2. Cache Check & Batching
        missing_texts = []
        cached_vectors = {}
        for idx, chunk in enumerate(all_chunks):
            cached_vec = self.cache.get(chunk.text, model)
            if cached_vec:
                cached_vectors[idx] = cached_vec
            else:
                missing_texts.append((idx, chunk.text))
                
        # 3. Provider Call
        total_tokens = 0
        if missing_texts:
            # We would batch here based on config.max_batch_size, but for architecture simple call
            texts = [t[1] for t in missing_texts]
            response = self.provider.embed(texts, model)
            total_tokens = response.total_tokens
            
            # Map back and update cache
            for i, (idx, text) in enumerate(missing_texts):
                vec = response.vectors[i]
                cached_vectors[idx] = vec
                self.cache.set(text, model, vec)
                
        # 4. Construct Output
        final_vectors = []
        for idx, chunk in enumerate(all_chunks):
            final_vectors.append(
                EmbeddingVector(
                    vector=cached_vectors[idx],
                    text=chunk.text,
                    metadata=chunk.metadata
                )
            )
            
        # 5. Telemetry
        latency_ms = int((time.perf_counter() - start_time) * 1000)
        cost = self._calculate_cost(total_tokens)
        
        self.telemetry.record_embedding(
            correlation_id=correlation_id,
            model=model,
            latency_ms=latency_ms,
            chunks=len(all_chunks),
            cost=cost
        )
        
        return EmbeddingResponse(
            vectors=final_vectors,
            model_used=model,
            total_tokens=total_tokens,
            cost=cost
        )
''', encoding="utf-8")

# 9. __init__.py
(emb_dir / "__init__.py").write_text('''"""
Enterprise Embedding Service
"""
from .exceptions import *
from .config import EmbeddingConfig
from .models import EmbeddingRequest, EmbeddingResponse, EmbeddingVector, Chunk
from .providers import EmbeddingProvider, OpenAIEmbeddingProvider
from .chunker import Chunker
from .cache import EmbeddingCache
from .telemetry import Telemetry
from .embedding_service import EmbeddingService
''', encoding="utf-8")

print("Created Enterprise Embedding Service files")
