"""
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
