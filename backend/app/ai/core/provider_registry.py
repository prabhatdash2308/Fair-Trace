from typing import Dict, Type
import structlog
from app.ai.core.llm_provider import BaseLLMProvider, OpenAIProvider

logger = structlog.get_logger(__name__)

class ProviderRegistry:
    """Registry to dynamically resolve LLM providers based on configuration."""
    
    _providers: Dict[str, BaseLLMProvider] = {}
    
    @classmethod
    def get_provider(cls, name: str = "openai") -> BaseLLMProvider:
        if name not in cls._providers:
            if name == "openai":
                cls._providers[name] = OpenAIProvider()
            else:
                raise ValueError(f"Unknown LLM provider: {name}")
                
        return cls._providers[name]
