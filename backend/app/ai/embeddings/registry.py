from typing import Dict, Type
from app.ai.embeddings.base import BaseEmbeddingProvider

class EmbeddingProviderRegistry:
    """Registry pattern to abstract provider instantiation from the service layer."""
    _providers: Dict[str, Type[BaseEmbeddingProvider]] = {}

    @classmethod
    def register(cls, name: str, provider_class: Type[BaseEmbeddingProvider]):
        cls._providers[name] = provider_class

    @classmethod
    def get_provider(cls, name: str, **kwargs) -> BaseEmbeddingProvider:
        if name not in cls._providers:
            raise ValueError(f"No provider registered with name '{name}'")
        return cls._providers[name](**kwargs)
