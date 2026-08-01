"""
Abstract provider interface and implementations.
"""
from abc import ABC, abstractmethod
from typing import List
from .models import ProviderResponse
from .exceptions import EmbeddingProviderError

class EmbeddingProvider(ABC):
    @abstractmethod
    def embed(self, texts: List[str], model: str) -> ProviderResponse:
        pass

class OpenAIEmbeddingProvider(EmbeddingProvider):
    def __init__(self, api_key: str = "dummy"):
        self.api_key = api_key
        
    def embed(self, texts: List[str], model: str) -> ProviderResponse:
        # Dummy implementation
        try:
            vectors = []
            for t in texts:
                # generate a dummy vector of 3 dimensions for tests
                vectors.append([0.1, 0.2, 0.3])
            
            # Dummy token math: roughly length of texts // 4
            tokens = sum(len(t) // 4 for t in texts)
            return ProviderResponse(vectors=vectors, total_tokens=tokens)
        except Exception as e:
            raise EmbeddingProviderError(f"Provider failed: {str(e)}") from e
