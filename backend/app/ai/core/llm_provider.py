from abc import ABC, abstractmethod
from typing import Any, Dict, Type
import json
import structlog
from pydantic import BaseModel

logger = structlog.get_logger(__name__)

class BaseLLMProvider(ABC):
    """Abstract Base Class for LLM Providers."""
    
    @abstractmethod
    async def generate_structured(
        self,
        system_prompt: str,
        developer_prompt: str,
        user_message: str,
        response_model: Type[BaseModel],
        model_name: str,
        temperature: float,
        max_tokens: int
    ) -> Dict[str, Any]:
        """
        Generates a structured JSON response matching the response_model schema.
        Returns a dictionary containing the parsed JSON, and usage statistics.
        """
        pass
    
    @abstractmethod
    def health(self) -> str:
        """Returns provider health status."""
        pass

class OpenAIProvider(BaseLLMProvider):
    """OpenAI Implementation using the official python SDK and strict structured outputs."""
    
    def __init__(self):
        try:
            from openai import AsyncOpenAI
            self.client = AsyncOpenAI()
        except ImportError:
            raise RuntimeError("openai package not installed.")
        
    async def generate_structured(
        self,
        system_prompt: str,
        developer_prompt: str,
        user_message: str,
        response_model: Type[BaseModel],
        model_name: str,
        temperature: float,
        max_tokens: int
    ) -> Dict[str, Any]:
        logger.debug(
            "calling_openai", 
            model=model_name, 
            response_model=response_model.__name__
        )
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        if developer_prompt:
            messages.append({"role": "developer", "content": developer_prompt})
        if user_message:
            messages.append({"role": "user", "content": user_message})

        try:
            response = await self.client.beta.chat.completions.parse(
                model=model_name,
                messages=messages,
                response_format=response_model,
                temperature=temperature,
                max_completion_tokens=max_tokens
            )
            
            message = response.choices[0].message
            
            if message.refusal:
                raise ValueError(f"Model refused to generate structured output: {message.refusal}")
            
            parsed_data = message.parsed
            
            return {
                "parsed_data": parsed_data,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                },
                "model_used": response.model
            }
            
        except Exception as e:
            logger.error("openai_provider_error", error=str(e))
            raise

    def health(self) -> str:
        # In a real scenario, this might verify API key presence
        return "healthy"
