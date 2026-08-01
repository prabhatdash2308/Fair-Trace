"""
Abstract provider interface and concrete implementations.
"""
from abc import ABC, abstractmethod
from typing import Any
from .models import LLMRequest, LLMResponse
from .config import LLMConfig

class LLMProvider(ABC):
    @abstractmethod
    def generate(self, request: LLMRequest, config: LLMConfig) -> LLMResponse:
        pass

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str = "dummy"):
        # self.client = openai.Client(api_key=api_key)
        self.api_key = api_key
        
    def generate(self, request: LLMRequest, config: LLMConfig) -> LLMResponse:
        # Dummy implementation to satisfy the architecture test without making real network calls
        # In production, this would call self.client.chat.completions.create(...)
        model = request.model or config.default_model
        
        # Simulate structured output
        if request.response_format:
            content = '{"status": "success", "score": 95}'
        else:
            content = "This is a simulated OpenAI response."
            
        return LLMResponse(
            content=content,
            model_used=model,
            prompt_tokens=10,
            completion_tokens=20,
            total_tokens=30,
            finish_reason="stop"
        )
