import re
from typing import List
from uuid import UUID

from config import settings
from models.db.document import Document
from models.enums import ChunkStrategy
from app.ai.chunking.base import BaseChunker
from app.ai.chunking.chunk_models import ChunkModel, ChunkMetadata
from app.ai.chunking.utils import estimate_tokens, generate_checksum
from app.ai.chunking.chunk_registry import ChunkRegistry

class SentenceChunker(BaseChunker):
    """
    Fallback Chunker: Splits text exclusively on sentence boundaries,
    grouping sentences until the token limit is reached, applying overlap.
    """
    
    @property
    def version(self) -> str:
        return "1.0"
        
    @property
    def strategy_name(self) -> str:
        return ChunkStrategy.SENTENCE.value

    def split_document(self, document: Document) -> List[ChunkModel]:
        text = document.parsed_text or ""
        
        # Extremely basic sentence splitting on period, question, exclamation.
        # Keeping delimiters attached to the sentence.
        sentences = re.split(r'(?<=[.!?])\s+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        chunks = []
        current_chunk_sentences = []
        current_tokens = 0
        chunk_index = 0
        
        # We need offsets too, which is harder when splitting.
        # We will track current offset in the original string.
        current_offset = 0
        
        for sentence in sentences:
            sent_tokens = estimate_tokens(sentence)
            
            # If a single sentence is huge, we have to just accept it in this fallback
            if current_tokens + sent_tokens > settings.chunk_size and current_chunk_sentences:
                # Flush chunk
                chunk_text = " ".join(current_chunk_sentences)
                # Compute approximate offset
                start_off = text.find(chunk_text, current_offset)
                if start_off == -1: start_off = current_offset
                end_off = start_off + len(chunk_text)
                current_offset = end_off
                
                metadata = ChunkMetadata(
                    parser_version=document.parser_version or "unknown",
                    chunker=self.strategy_name,
                    chunk_version=self.version,
                    strategy_version=self.version
                )
                
                chunks.append(ChunkModel(
                    document_id=document.id,
                    chunk_index=chunk_index,
                    text=chunk_text,
                    start_offset=start_off,
                    end_offset=end_off,
                    token_estimate=current_tokens,
                    character_count=len(chunk_text),
                    word_count=len(chunk_text.split()),
                    checksum=generate_checksum(document.id, chunk_index, chunk_text),
                    metadata=metadata
                ))
                
                chunk_index += 1
                
                # Overlap logic: keep last N sentences that fit in chunk_overlap
                overlap_sentences = []
                overlap_tokens = 0
                for s in reversed(current_chunk_sentences):
                    t = estimate_tokens(s)
                    if overlap_tokens + t <= settings.chunk_overlap:
                        overlap_sentences.insert(0, s)
                        overlap_tokens += t
                    else:
                        break
                        
                current_chunk_sentences = overlap_sentences
                current_tokens = overlap_tokens
                # Re-adjust offset slightly backwards (approximate for overlap)
                if overlap_sentences:
                    overlap_text = " ".join(overlap_sentences)
                    current_offset = max(0, start_off + len(chunk_text) - len(overlap_text))
            
            current_chunk_sentences.append(sentence)
            current_tokens += sent_tokens
            
        # Flush remaining
        if current_chunk_sentences:
            chunk_text = " ".join(current_chunk_sentences)
            start_off = text.find(chunk_text, current_offset)
            if start_off == -1: start_off = current_offset
            end_off = start_off + len(chunk_text)
            
            metadata = ChunkMetadata(
                parser_version=document.parser_version or "unknown",
                chunker=self.strategy_name,
                chunk_version=self.version,
                strategy_version=self.version
            )
            
            chunks.append(ChunkModel(
                document_id=document.id,
                chunk_index=chunk_index,
                text=chunk_text,
                start_offset=start_off,
                end_offset=end_off,
                token_estimate=current_tokens,
                character_count=len(chunk_text),
                word_count=len(chunk_text.split()),
                checksum=generate_checksum(document.id, chunk_index, chunk_text),
                metadata=metadata
            ))
            
        return chunks

ChunkRegistry.register(ChunkStrategy.SENTENCE, SentenceChunker)
