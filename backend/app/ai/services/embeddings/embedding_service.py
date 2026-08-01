"""
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
