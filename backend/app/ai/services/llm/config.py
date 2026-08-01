"""
Configuration models for the LLM Service.
"""
from pydantic import BaseModel, Field
from typing import Optional

class LLMConfig(BaseModel):
    default_model: str = "gpt-4o"
    fallback_model: str = "gpt-4o-mini"
    temperature: float = Field(default=0.0, ge=0.0, le=2.0)
    max_tokens: int = Field(default=4000, gt=0)
    request_timeout_seconds: float = 60.0
    max_retries: int = 3
