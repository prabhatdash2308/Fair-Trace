"""
Data models for the Prompt Management System.
"""
from pydantic import BaseModel, Field
from typing import List

class PromptMetadata(BaseModel):
    """Metadata describing a registered prompt."""
    name: str
    version: str
    description: str
    owner_agent: str
    required_variables: List[str] = Field(default_factory=list)
    system_prompt_path: str
    user_prompt_path: str
