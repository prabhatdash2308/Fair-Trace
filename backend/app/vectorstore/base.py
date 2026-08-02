from abc import ABC, abstractmethod
from typing import List, Dict, Any
from app.vectorstore.models import VectorPoint

class BaseVectorStore(ABC):
    """Abstract interface for Vector Store operations."""

    @abstractmethod
    async def initialize_collection(self) -> None:
        """Idempotent initialization of the vector collection."""
        pass

    @abstractmethod
    async def upsert_batch(self, points: List[VectorPoint]) -> None:
        """Upsert a batch of vectors. Should validate vectors before insertion."""
        pass

    @abstractmethod
    async def search(self, vector: List[float], top_k: int, score_threshold: float, filter_conditions: Any = None) -> List[Any]:
        """Search the vector store for similar vectors."""
        pass

    @abstractmethod
    async def health(self) -> Dict[str, Any]:
        """Check vector store health, permissions, and schema configuration."""
        pass
