import time
from typing import List, Dict, Set
from app.ai.retrieval.models import RetrievedChunk, ContextBundle, ContextBundleStatistics, ContextBundleMetadata
from app.ai.retrieval.exceptions import InvalidPayloadError, ContextLimitError
import structlog

logger = structlog.get_logger(__name__)

class ContextCompressor:
    """Stubs for future enterprise compression algorithms."""
    
    @staticmethod
    def compress(chunks: List[RetrievedChunk]) -> List[RetrievedChunk]:
        # Phase 11.5: No Compression
        # Later: Redundant Chunk Removal, Heading Merging, Semantic Compression
        return chunks

class ContextBuilder:
    def __init__(self, max_context_tokens: int):
        self.max_context_tokens = max_context_tokens

    def _validate_payload(self, chunk: RetrievedChunk):
        """Strict metadata validation before it enters LangGraph."""
        required = [
            chunk.document_id, chunk.chunk_id, chunk.checksum, 
            chunk.embedding_model, chunk.token_count
        ]
        if not all(required):
            raise InvalidPayloadError(f"Incomplete payload for chunk {getattr(chunk, 'chunk_id', 'UNKNOWN')}")
            
    def build(self, chunks: List[RetrievedChunk]) -> ContextBundle:
        """Assembles the Context Bundle from ranked chunks."""
        start_time = time.time()
        
        seen_checksums: Set[str] = set()
        seen_chunk_ids: Set[str] = set()
        seen_vector_ids: Set[str] = set()
        
        valid_chunks: List[RetrievedChunk] = []
        total_tokens = 0
        
        # 1. Deduplicate & Validate & Enforce Token Limits
        for chunk in chunks:
            self._validate_payload(chunk)
            
            # Deduplicate
            if chunk.checksum in seen_checksums or chunk.chunk_id in seen_chunk_ids or chunk.vector_id in seen_vector_ids:
                continue
                
            # Token Bound
            if total_tokens + chunk.token_count > self.max_context_tokens:
                logger.warning("context_token_limit_reached", limit=self.max_context_tokens)
                break
                
            seen_checksums.add(chunk.checksum)
            seen_chunk_ids.add(chunk.chunk_id)
            seen_vector_ids.add(chunk.vector_id)
            
            valid_chunks.append(chunk)
            total_tokens += chunk.token_count
            
        # 2. Compression (Stubbed)
        compressed_chunks = ContextCompressor.compress(valid_chunks)
        
        # 3. Assemble Metadata
        document_ids: Set[str] = {c.document_id for c in compressed_chunks}
        headings: Set[str] = {c.heading for c in compressed_chunks if c.heading}
        sections: Set[str] = {c.section for c in compressed_chunks if c.section}
        
        # 4. Construct String Context (For LangGraph insertion later)
        combined_text = "\n\n---\n\n".join([f"[{c.document_type}] {c.heading or ''} - {c.section or ''}\n{c.text}" for c in compressed_chunks])
        
        build_time_ms = int((time.time() - start_time) * 1000)
        
        return ContextBundle(
            statistics=ContextBundleStatistics(
                total_chunks=len(compressed_chunks),
                total_documents=len(document_ids),
                total_tokens=total_tokens,
                build_time_ms=build_time_ms
            ),
            metadata=ContextBundleMetadata(
                headings=list(headings),
                sections=list(sections)
            ),
            chunks=compressed_chunks,
            combined_context=combined_text
        )
