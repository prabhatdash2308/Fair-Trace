from abc import ABC, abstractmethod
from typing import List, Dict, Any

from app.ai.embeddings.models import ChunkToEmbed, BatchEmbeddingResponse

class BaseEmbeddingProvider(ABC):
    """
    Abstract interface for enterprise embedding providers.
    Every provider must conform to this boundary.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Name of the provider (e.g., 'OpenAI', 'Azure', 'Mock')."""
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Name of the model being used (e.g., 'text-embedding-3-small')."""
        pass

    @property
    @abstractmethod
    def model_version(self) -> str:
        """Version of the model or provider integration."""
        pass
        
    @property
    @abstractmethod
    def dimension(self) -> int:
        """Dimension of the vectors produced by this provider."""
        pass

    @abstractmethod
    async def embed_batch(self, chunks: List[ChunkToEmbed]) -> BatchEmbeddingResponse:
        """
        Takes a batch of validated text chunks and returns their vectors,
        along with complete token accounting and execution metadata.
        """
        pass

    @abstractmethod
    async def health(self) -> Dict[str, Any]:
        """
        Returns the health status of the provider.
        Should make a minimal, inexpensive call to verify connectivity.
        """
        pass
