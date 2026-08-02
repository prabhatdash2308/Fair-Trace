import re
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import settings
from models.db.document import Document
from models.enums import ChunkStrategy
from app.ai.chunking.base import BaseChunker
from app.ai.chunking.chunk_models import ChunkModel, ChunkMetadata
from app.ai.chunking.utils import estimate_tokens, generate_checksum, extract_hr_metadata, detect_document_type
from app.ai.chunking.chunk_registry import ChunkRegistry

class SemanticChunker(BaseChunker):
    """
    Primary Chunker: Uses heuristics to detect HR sections, headings,
    and structured elements (lists, tables). Protects semantic boundaries.
    """
    
    @property
    def version(self) -> str:
        return "1.0"
        
    @property
    def strategy_name(self) -> str:
        return ChunkStrategy.SEMANTIC.value

    def split_document(self, document: Document) -> List[ChunkModel]:
        text = document.parsed_text or ""
        
        # 1. Detect HR metadata and doc type
        hr_metadata = extract_hr_metadata(text)
        doc_type = detect_document_type(text)
        
        # 2. Heuristic splitting: Find safe breakpoints.
        # We want to avoid breaking inside tables or lists if possible.
        # Tables often have "|" or "---". Lists start with "-" or "*".
        # We will use RecursiveCharacterTextSplitter but with smarter separators.
        
        # Protect specific headings by adding them as primary separators.
        # Common HR sections:
        hr_sections = [
            "Employee Information", "Employee Goals", "Key Responsibilities",
            "Performance Summary", "Performance Rating", "Manager Feedback",
            "Peer Feedback", "Self Assessment", "Strengths", 
            "Areas for Improvement", "Development Plan", "Recommendations",
            "Overall Comments"
        ]
        
        # We can dynamically inject these as separators by pre-processing the text
        # or just adding them to the splitter.
        # Langchain splits exactly on separators, so adding exact strings might be too rigid (case sensitivity).
        # Instead, we rely on \n\n as the primary, and use regex to identify the "current heading".
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            length_function=estimate_tokens,
            separators=["\n\n", "\n", ". ", " ", ""],
            add_start_index=True
        )
        
        docs = splitter.create_documents([text])
        chunks = []
        
        current_heading = None
        
        for idx, d in enumerate(docs):
            chunk_text = d.page_content
            start_off = d.metadata.get("start_index", 0)
            end_off = start_off + len(chunk_text)
            
            # Heuristically detect if this chunk starts with or contains an HR heading
            for sec in hr_sections:
                # Basic check: if the section name appears followed by a newline or colon
                if re.search(rf"(?i)^\s*{sec}\s*[:\n]", chunk_text) or re.search(rf"(?i)\n\s*{sec}\s*[:\n]", chunk_text):
                    current_heading = sec
                    break
            
            # Calculate a pseudo semantic confidence
            # High if it starts exactly on a paragraph boundary and doesn't sever a markdown list
            confidence = 0.8
            if re.match(r"^[\-\*]\s", chunk_text):
                # Starts mid-list
                confidence = 0.5
            if current_heading:
                confidence += 0.1
            confidence = min(1.0, confidence)
            
            metadata_dict = {
                "parser_version": document.parser_version or "unknown",
                "chunker": self.strategy_name,
                "chunk_version": self.version,
                "strategy_version": self.version,
                "document_type": doc_type,
                "heading": current_heading
            }
            # Merge in HR metadata
            metadata_dict.update(hr_metadata)
            
            metadata = ChunkMetadata(**metadata_dict)
            
            chunks.append(ChunkModel(
                document_id=document.id,
                chunk_index=idx,
                text=chunk_text,  # 100% identical to source, heading is in metadata
                start_offset=start_off,
                end_offset=end_off,
                token_estimate=estimate_tokens(chunk_text),
                character_count=len(chunk_text),
                word_count=len(chunk_text.split()),
                checksum=generate_checksum(document.id, idx, chunk_text),
                semantic_confidence=round(confidence, 2),
                metadata=metadata
            ))
            
        return chunks

ChunkRegistry.register(ChunkStrategy.SEMANTIC, SemanticChunker)
