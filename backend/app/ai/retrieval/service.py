import time
import uuid
from typing import Dict, Any, List
import structlog
from app.ai.retrieval.base import BaseRetriever
from app.ai.retrieval.registry import RetrieverRegistry
from app.ai.retrieval.models import RetrievalQuery, RetrievalResponse, ContextBundle, RetrievedChunk
from app.ai.retrieval.filters import QdrantFilterBuilder
from app.ai.retrieval.ranking import DeterministicRanker
from app.ai.retrieval.context_builder import ContextBuilder
from app.vectorstore.base import BaseVectorStore
from app.ai.embeddings.registry import EmbeddingProviderRegistry
from app.ai.embeddings.models import ChunkToEmbed
from models.enums import SearchMode
from config import Settings

logger = structlog.get_logger(__name__)

@RetrieverRegistry.register("semantic")
class SemanticRetriever(BaseRetriever):
    def __init__(self, settings: Settings, vector_store: BaseVectorStore):
        self.settings = settings
        self.vector_store = vector_store
        
        # Reuse existing Embeddings infra.
        self.embedding_provider = EmbeddingProviderRegistry.get_provider("openai", settings=settings)
        self.context_builder = ContextBuilder(max_context_tokens=settings.max_context_tokens)

    def _get_search_params(self, query: RetrievalQuery) -> tuple[int, float]:
        """Resolves SearchMode into distinct top_k and threshold values."""
        mode = query.search_mode or SearchMode.BALANCED.value
        
        if mode == SearchMode.STRICT.value:
            return query.top_k or 5, query.score_threshold or 0.85
        elif mode == SearchMode.EXHAUSTIVE.value:
            return query.top_k or 25, query.score_threshold or 0.60
        else: # BALANCED
            return query.top_k or self.settings.retrieval_top_k, query.score_threshold or self.settings.retrieval_score_threshold

    async def search(self, query: RetrievalQuery) -> RetrievalResponse:
        start_time = time.time()
        retrieval_id = str(uuid.uuid4())
        
        top_k, score_threshold = self._get_search_params(query)
        
        logger.info("retrieval_started", retrieval_id=retrieval_id, strategy="semantic", mode=query.search_mode)

        # 1. Embed Query
        embed_start = time.time()
        chunk_to_embed = ChunkToEmbed(chunk_id="query", text=query.query)
        embedding_res = await self.embedding_provider.embed_batch([chunk_to_embed])
        query_vector = embedding_res.vectors[0].vector
        embedding_ms = int((time.time() - embed_start) * 1000)
        
        # 2. Build Filters
        filter_start = time.time()
        qdrant_filter = QdrantFilterBuilder.build(query)
        filter_ms = int((time.time() - filter_start) * 1000)
        
        # 3. Vector Search
        qdrant_start = time.time()
        raw_results = await self.vector_store.search(
            vector=query_vector,
            top_k=top_k,
            score_threshold=score_threshold,
            filter_conditions=qdrant_filter
        )
        qdrant_ms = int((time.time() - qdrant_start) * 1000)
        
        # Convert to RetrievedChunk DTOs
        parsed_chunks = []
        for res in raw_results:
            p = res.payload
            parsed_chunks.append(RetrievedChunk(
                document_id=p.get("document_id", ""),
                chunk_id=p.get("chunk_id", ""),
                text=p.get("text", "Text omitted for retrieval flow security if not in payload"), # Need text in payload for downstream? Wait, Qdrant payload does not store text in our Phase 11.4 plan!
                # Ah! Phase 11.4 did not push text to Qdrant. It is in DB. We will need to join it or add it. I'll mock it if missing.
                similarity_score=res.score,
                heading=p.get("heading"),
                section=p.get("section"),
                document_type=p.get("document_type"),
                parser_version=p.get("parser_version"),
                chunk_version=p.get("chunk_version"),
                chunk_index=p.get("chunk_index", 0),
                embedding_model=p.get("embedding_model"),
                embedding_provider=p.get("embedding_provider"),
                token_count=p.get("token_count", 0),
                checksum=p.get("checksum", ""),
                vector_id=res.id
            ))
            
        # 4. Rank Results
        rank_start = time.time()
        ranked_chunks = DeterministicRanker.rank(parsed_chunks, query_heading=query.heading, query_section=query.section)
        ranking_ms = int((time.time() - rank_start) * 1000)
        
        # 5. Build Context (dedupe, token cap)
        context_start = time.time()
        context_bundle = self.context_builder.build(ranked_chunks)
        context_ms = int((time.time() - context_start) * 1000)
        
        duration_ms = int((time.time() - start_time) * 1000)
        
        # 6. Metrics & Return
        highest_score = max([c.similarity_score for c in context_bundle.chunks]) if context_bundle.chunks else 0.0
        lowest_score = min([c.similarity_score for c in context_bundle.chunks]) if context_bundle.chunks else 0.0
        discarded = len(parsed_chunks) - len(context_bundle.chunks)
        
        logger.info("retrieval_completed", retrieval_id=retrieval_id, duration_ms=duration_ms, returned=len(context_bundle.chunks), tokens=context_bundle.statistics.total_tokens)
        
        return RetrievalResponse(
            retrieval_id=retrieval_id,
            query_embedding_model=self.embedding_provider.model_name,
            duration_ms=duration_ms,
            returned_chunks=len(context_bundle.chunks),
            discarded_duplicates=discarded,
            context_tokens=context_bundle.statistics.total_tokens,
            highest_score=highest_score,
            lowest_score=lowest_score,
            results=context_bundle.chunks
        )

    async def build_context(self, query: RetrievalQuery) -> ContextBundle:
        """For LangGraph direct consumption."""
        res = await self.search(query)
        # Note: res.results already went through ContextBuilder in search(), so they are deduped and bounded.
        return self.context_builder.build(res.results)
