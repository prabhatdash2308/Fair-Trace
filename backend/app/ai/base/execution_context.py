"""
ExecutionContext Model
Provides runtime context for an agent execution.
"""
from pydantic import BaseModel, Field
from pydantic.types import UUID4
from datetime import datetime, timezone
import uuid

class ExecutionContext(BaseModel):
    """
    Runtime context passed to agents during execution.
    Contains identifiers and retry state.
    """
    pipeline_id: UUID4
    correlation_id: str
    current_agent: str
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    retry_count: int = Field(default=0, ge=0)
