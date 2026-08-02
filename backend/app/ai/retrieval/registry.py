from typing import Dict, Type
from app.ai.retrieval.base import BaseRetriever
from config import Settings

class RetrieverRegistry:
    """Enterprise Factory for resolving Retrieval Strategies dynamically."""
    
    _registry: Dict[str, Type[BaseRetriever]] = {}

    @classmethod
    def register(cls, strategy: str):
        def wrapper(retriever_class: Type[BaseRetriever]):
            cls._registry[strategy] = retriever_class
            return retriever_class
        return wrapper

    @classmethod
    def get_retriever(cls, strategy: str, **kwargs) -> BaseRetriever:
        retriever_class = cls._registry.get(strategy)
        if not retriever_class:
            raise ValueError(f"Retriever strategy '{strategy}' not registered.")
        return retriever_class(**kwargs)
