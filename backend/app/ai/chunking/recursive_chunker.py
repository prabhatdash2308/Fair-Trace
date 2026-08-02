from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import settings
from models.db.document import Document
from models.enums import ChunkStrategy
from app.ai.chunking.base import BaseChunker
from app.ai.chunking.chunk_models import ChunkModel, ChunkMetadata
from app.ai.chunking.utils import estimate_tokens, generate_checksum
from app.ai.chunking.chunk_registry import ChunkRegistry

class RecursiveChunker(BaseChunker):
    """
    Default Chunker: Uses RecursiveCharacterTextSplitter from LangChain.
    Tries paragraphs -> sentences -> words.
    """
    
    @property
    def version(self) -> str:
        return "1.0"
        
    @property
    def strategy_name(self) -> str:
        return ChunkStrategy.RECURSIVE.value

    def split_document(self, document: Document) -> List[ChunkModel]:
        text = document.parsed_text or ""
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            length_function=estimate_tokens,
            separators=["\n\n", "\n", ". ", " ", ""],
            add_start_index=True
        )
        
        # We can get start offsets by passing add_start_index=True
        # but Langchain's create_documents handles this nicely
        docs = splitter.create_documents([text])
        
        chunks = []
        for idx, d in enumerate(docs):
            chunk_text = d.page_content
            # Langchain stores start index in metadata if add_start_index=True, but let's just find it
            # If not provided, we just find the first occurrence from the previous end
            start_off = d.metadata.get("start_index", -1)
            if start_off == -1:
                # Fallback manual tracking
                prev_off = chunks[-1].start_offset if chunks else 0
                start_off = text.find(chunk_text, prev_off)
                if start_off == -1: start_off = prev_off
                
            end_off = start_off + len(chunk_text)
            
            metadata = ChunkMetadata(
                parser_version=document.parser_version or "unknown",
                chunker=self.strategy_name,
                chunk_version=self.version,
                strategy_version=self.version
            )
            
            chunks.append(ChunkModel(
                document_id=document.id,
                chunk_index=idx,
                text=chunk_text,
                start_offset=start_off,
                end_offset=end_off,
                token_estimate=estimate_tokens(chunk_text),
                character_count=len(chunk_text),
                word_count=len(chunk_text.split()),
                checksum=generate_checksum(document.id, idx, chunk_text),
                metadata=metadata
            ))
            
        return chunks

ChunkRegistry.register(ChunkStrategy.RECURSIVE, RecursiveChunker)
