from abc import ABC, abstractmethod
from typing import List
from app.ai.chunking.chunk_models import ChunkModel
from models.db.document import Document

class BaseChunker(ABC):
    """
    Abstract Base Class for all Chunking Strategies.
    """
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Returns the version of this chunker logic."""
        pass
        
    @property
    @abstractmethod
    def strategy_name(self) -> str:
        """Returns the chunk strategy name."""
        pass

    @abstractmethod
    def split_document(self, document: Document) -> List[ChunkModel]:
        """
        Splits a parsed Document into a list of ChunkModel objects.
        
        Args:
            document: The Document database record containing parsed_text.
            
        Returns:
            List of ChunkModels ready for validation and insertion.
        """
        pass
