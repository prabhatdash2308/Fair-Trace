import time
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import structlog
from sqlalchemy.orm import Session

from models.db.document_chunk import DocumentChunk
from models.enums import EmbeddingStatus
from app.ai.embeddings.registry import EmbeddingProviderRegistry
from app.ai.embeddings.models import ChunkToEmbed
from app.ai.embeddings.batcher import Batcher
from app.vectorstore.base import BaseVectorStore
from app.vectorstore.models import VectorPoint
from config import Settings

logger = structlog.get_logger(__name__)

class EmbeddingService:
    def __init__(self, db: Session, settings: Settings, vector_store: BaseVectorStore):
        self.db = db
        self.settings = settings
        self.vector_store = vector_store
        # We explicitly lookup the provider configured in registry (Day-1 Abstraction)
        self.provider = EmbeddingProviderRegistry.get_provider(
            "openai", settings=settings
        )
        self.batch_size = settings.openai_embedding_batch_size

    async def embed_document(self, document_id: str, user_id: str, organization_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Idempotent entrypoint to embed a document's chunks.
        Skips already EMBEDDED chunks.
        """
        start_time = time.time()
        
        # 1. Fetch eligible chunks
        chunks = self.db.query(DocumentChunk).filter(
            DocumentChunk.document_id == document_id,
            DocumentChunk.embedding_status.notin_([EmbeddingStatus.EMBEDDED.value, EmbeddingStatus.QUEUED.value])
        ).order_by(DocumentChunk.chunk_index).all()
        
        # Or chunks that have None as embedding_status (new)
        if not chunks:
            chunks = self.db.query(DocumentChunk).filter(
                DocumentChunk.document_id == document_id,
                DocumentChunk.embedding_status.is_(None)
            ).order_by(DocumentChunk.chunk_index).all()

        if not chunks:
            return {
                "status": "completed",
                "document_id": str(document_id),
                "chunks_total": 0,
                "chunks_embedded": 0,
                "chunks_skipped": 0,
                "chunks_failed": 0,
                "batches": 0,
                "embedding_model": self.provider.model_name,
                "provider": self.provider.provider_name,
                "dimensions": self.provider.dimension,
                "tokens": 0,
                "estimated_cost_usd": 0.0,
                "duration_ms": 0,
                "collection": self.settings.QDRANT_COLLECTION
            }

        # Mark all as PROCESSING (idempotency safety)
        for c in chunks:
            c.embedding_status = EmbeddingStatus.PROCESSING.value
        self.db.commit()

        total_embedded = 0
        total_failed = 0
        total_tokens = 0
        total_cost = 0.0
        batch_count = 0

        # Transform to internal models
        embed_dtos = [ChunkToEmbed(chunk_id=str(c.id), text=c.text) for c in chunks]
        
        # 2. Batch and Validate
        batches = Batcher.validate_and_batch(embed_dtos, self.batch_size)

        for batch in batches:
            batch_count += 1
            try:
                # 3. Request Embeddings
                response = await self.provider.embed_batch(batch)
                total_tokens += response.accounting.total_tokens
                total_cost += response.accounting.estimated_cost_usd

                # 4. Prepare Vector points for Qdrant
                vector_points = []
                for vec in response.vectors:
                    # Find original chunk to build payload
                    chunk_orm = next((c for c in chunks if str(c.id) == vec.chunk_id), None)
                    if not chunk_orm:
                        continue
                        
                    payload = {
                        "document_id": str(chunk_orm.document_id),
                        "chunk_id": str(chunk_orm.id),
                        "organization_id": str(organization_id) if organization_id else None,
                        "user_id": str(user_id),
                        "heading": chunk_orm.metadata_.get("heading"),
                        "section": chunk_orm.metadata_.get("section"),
                        "document_type": chunk_orm.metadata_.get("document_type"),
                        "parser_version": chunk_orm.metadata_.get("parser_version"),
                        "chunk_version": chunk_orm.metadata_.get("chunk_version"),
                        "embedding_model": response.model,
                        "embedding_provider": response.provider,
                        "checksum": chunk_orm.checksum,
                        "created_at": datetime.now(timezone.utc).isoformat(),
                        "token_count": chunk_orm.token_estimate
                    }
                    
                    vector_points.append(
                        VectorPoint(id=vec.chunk_id, vector=vec.vector, payload=payload)
                    )

                # 5. Upsert to Qdrant
                await self.vector_store.upsert_batch(vector_points)

                # 6. Update Database
                for vec in response.vectors:
                    chunk_orm = next((c for c in chunks if str(c.id) == vec.chunk_id), None)
                    if chunk_orm:
                        chunk_orm.embedding_status = EmbeddingStatus.EMBEDDED.value
                        chunk_orm.vector_id = vec.chunk_id
                        chunk_orm.embedding_model = response.model
                        chunk_orm.embedding_provider = response.provider
                        chunk_orm.embedding_version = response.version
                        chunk_orm.embedding_dimensions = self.provider.dimension
                        chunk_orm.embedding_created_at = datetime.now(timezone.utc)
                        chunk_orm.embedding_duration_ms = response.duration_ms
                        chunk_orm.token_count = chunk_orm.token_estimate
                        chunk_orm.embedding_checksum = chunk_orm.checksum
                        chunk_orm.embedding_error = None
                
                self.db.commit()
                total_embedded += len(batch)

            except Exception as e:
                logger.error("batch_embedding_failed", error=str(e), batch_index=batch_count)
                # Mark batch as FAILED
                for dto in batch:
                    chunk_orm = next((c for c in chunks if str(c.id) == dto.chunk_id), None)
                    if chunk_orm:
                        chunk_orm.embedding_status = EmbeddingStatus.FAILED.value
                        chunk_orm.embedding_error = str(e)
                self.db.commit()
                total_failed += len(batch)

        duration_ms = int((time.time() - start_time) * 1000)
        
        logger.info("document_embedded", 
            document_id=document_id, 
            chunks_total=len(chunks), 
            embedded=total_embedded, 
            failed=total_failed, 
            tokens=total_tokens, 
            duration_ms=duration_ms
        )

        return {
            "status": "completed",
            "document_id": str(document_id),
            "chunks_total": len(chunks),
            "chunks_embedded": total_embedded,
            "chunks_skipped": 0,  # We excluded them from `chunks` list at the start
            "chunks_failed": total_failed,
            "batches": batch_count,
            "embedding_model": self.provider.model_name,
            "provider": self.provider.provider_name,
            "dimensions": self.provider.dimension,
            "tokens": total_tokens,
            "estimated_cost_usd": total_cost,
            "duration_ms": duration_ms,
            "collection": self.settings.QDRANT_COLLECTION
        }
