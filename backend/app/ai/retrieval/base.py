from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from app.ai.retrieval.models import RetrievalQuery, RetrievalResponse, ContextBundle

class BaseRetriever(ABC):
    """Abstract interface for Retrieval Engines."""
    
    @abstractmethod
    async def search(self, query: RetrievalQuery) -> RetrievalResponse:
        """Executes the full retrieval flow."""
        pass
    
    @abstractmethod
    async def build_context(self, query: RetrievalQuery) -> ContextBundle:
        """Executes retrieval and constructs a bundled context string for LLM insertion."""
        pass
