"""
AgentResult Model
Tracks the execution metrics and outcome of a single agent run.
"""
from pydantic import BaseModel, Field
from typing import List
from app.ai.state.review_state import ExecutionStatus

class AgentResult(BaseModel):
    """
    Encapsulates the result and telemetry of an agent execution.
    """
    success: bool = False
    latency_ms: int = Field(default=0, ge=0)
    tokens_used: int = Field(default=0, ge=0)
    estimated_cost: float = Field(default=0.0, ge=0.0)
    warnings: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    execution_status: ExecutionStatus = ExecutionStatus.PENDING
