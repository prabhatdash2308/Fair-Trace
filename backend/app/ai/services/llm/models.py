"""
Data models for LLM requests and responses.
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, Type

class LLMRequest(BaseModel):
    system_prompt: str
    user_prompt: str
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    response_format: Optional[Type[BaseModel]] = None
    stream: bool = False

class LLMResponse(BaseModel):
    content: str
    model_used: str
    prompt_tokens: int = Field(default=0, ge=0)
    completion_tokens: int = Field(default=0, ge=0)
    total_tokens: int = Field(default=0, ge=0)
    finish_reason: str = "stop"
    structured_data: Optional[Any] = None
