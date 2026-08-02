from typing import Dict, Type
from app.ai.chunking.base import BaseChunker
from models.enums import ChunkStrategy

class ChunkRegistry:
    """Registry to map ChunkStrategy enums to Chunker implementations."""
    
    _registry: Dict[ChunkStrategy, Type[BaseChunker]] = {}

    @classmethod
    def register(cls, strategy: ChunkStrategy, chunker_cls: Type[BaseChunker]):
        cls._registry[strategy] = chunker_cls

    @classmethod
    def get_chunker(cls, strategy: ChunkStrategy) -> BaseChunker:
        chunker_cls = cls._registry.get(strategy)
        if not chunker_cls:
            raise ValueError(f"No chunker registered for strategy: {strategy}")
        return chunker_cls()
