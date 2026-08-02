import time
import structlog
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models.db.document import Document
from models.db.document_chunk import DocumentChunk
from models.enums import ChunkStrategy, ChunkStatus, ParsingStatus
from app.ai.chunking.chunk_registry import ChunkRegistry
from app.ai.chunking.chunk_models import ChunkStatistics
from app.ai.chunking.validator import ChunkValidator
from app.ai.chunking.exceptions import ChunkingError

logger = structlog.get_logger(__name__)

class ChunkService:
    def __init__(self, db: Session):
        self.db = db

    def chunk_document(self, document_id: UUID, user_id: UUID, strategy: ChunkStrategy = ChunkStrategy.SEMANTIC) -> ChunkStatistics:
        """
        Orchestrates the entire chunking pipeline for a document.
        """
        start_time = time.time()
        
        # 1. Load Document
        document = self.db.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
            
        if document.owner_id != user_id:
            raise HTTPException(status_code=404, detail="Document not found")
            
        if document.parsing_status != ParsingStatus.PARSED:
            raise HTTPException(status_code=400, detail="Document is not in PARSED state")
            
        if not document.parsed_text:
            raise HTTPException(status_code=400, detail="Document has no parsed text to chunk")

        # 2. Get Chunker
        chunker = ChunkRegistry.get_chunker(strategy)
        
        # 3. Split
        try:
            raw_chunks = chunker.split_document(document)
        except Exception as e:
            logger.error("chunking_failed", error=str(e), document_id=str(document_id))
            raise ChunkingError(f"Chunking failed: {str(e)}")

        # 4. Validate
        ChunkValidator.validate(raw_chunks)
        
        # 5. Persist to DB, filtering duplicates
        persisted_count = 0
        duplicates = 0
        tokens_total = 0
        chars_total = 0
        words_total = 0
        largest = 0
        smallest = float('inf')
        
        for c in raw_chunks:
            tokens_total += c.token_estimate
            chars_total += c.character_count
            words_total += c.word_count
            if c.token_estimate > largest: largest = c.token_estimate
            if c.token_estimate < smallest: smallest = c.token_estimate
            
            db_chunk = DocumentChunk(
                document_id=c.document_id,
                chunk_index=c.chunk_index,
                start_offset=c.start_offset,
                end_offset=c.end_offset,
                text=c.text,
                token_estimate=c.token_estimate,
                character_count=c.character_count,
                word_count=c.word_count,
                checksum=c.checksum,
                strategy=chunker.strategy_name,
                semantic_confidence=c.semantic_confidence,
                status=ChunkStatus.VALIDATED.value,
                metadata_=c.metadata.model_dump()
            )
            
            self.db.add(db_chunk)
            try:
                self.db.commit()
                persisted_count += 1
            except IntegrityError:
                self.db.rollback()
                duplicates += 1
                
        if smallest == float('inf'): smallest = 0
        
        duration_ms = int((time.time() - start_time) * 1000)
        
        stats = ChunkStatistics(
            status="completed",
            strategy=chunker.strategy_name,
            chunk_count=persisted_count,
            duplicates_removed=duplicates,
            average_tokens=tokens_total // max(1, len(raw_chunks)),
            average_words=words_total // max(1, len(raw_chunks)),
            average_chars=chars_total // max(1, len(raw_chunks)),
            largest_chunk=largest,
            smallest_chunk=smallest,
            processing_ms=duration_ms,
            document_id=document_id,
            compression_ratio=round((chars_total / max(1, len(document.parsed_text))), 2)
        )
        
        # 6. Log metrics
        logger.info(
            "chunking_completed",
            document_id=str(document_id),
            user_id=str(user_id),
            strategy=chunker.strategy_name,
            chunks=persisted_count,
            average_tokens=stats.average_tokens,
            largest_chunk=largest,
            smallest_chunk=smallest,
            duplicates=duplicates,
            processing_ms=duration_ms,
            status="completed"
        )
        
        return stats
