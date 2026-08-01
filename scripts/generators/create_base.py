import os
from pathlib import Path

base_dir = Path("backend/app/ai/base")
base_dir.mkdir(parents=True, exist_ok=True)

# 1. __init__.py
(base_dir / "__init__.py").write_text('''"""
AI Execution Framework Base Module
"""
from .exceptions import AgentExecutionError, StateValidationError, PromptLoadError, LLMExecutionError, RetryExceededError
from .agent_result import AgentResult
from .execution_context import ExecutionContext
from .base_agent import BaseAgent
''', encoding="utf-8")

# 2. exceptions.py
(base_dir / "exceptions.py").write_text('''"""
Custom exceptions for the AI Execution Framework.
"""

class AgentExecutionError(Exception):
    """Base exception for all agent execution errors."""
    pass

class StateValidationError(AgentExecutionError):
    """Raised when the ReviewState fails validation before execution."""
    pass

class PromptLoadError(AgentExecutionError):
    """Raised when an agent fails to load its required prompt templates."""
    pass

class LLMExecutionError(AgentExecutionError):
    """Raised when the underlying LLM call fails."""
    pass

class RetryExceededError(AgentExecutionError):
    """Raised when an agent exceeds its maximum retry attempts."""
    pass
''', encoding="utf-8")

# 3. agent_result.py
(base_dir / "agent_result.py").write_text('''"""
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
''', encoding="utf-8")

# 4. execution_context.py
(base_dir / "execution_context.py").write_text('''"""
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
''', encoding="utf-8")

# 5. base_agent.py
(base_dir / "base_agent.py").write_text('''"""
BaseAgent Abstract Class
Enterprise execution framework orchestrating agent lifecycle, logging, retries, and telemetry.
"""
import logging
import time
from abc import ABC, abstractmethod
from typing import Optional, Any
from pydantic import ValidationError

from app.ai.state.review_state import ReviewState, PipelineStatus, ExecutionStatus
from .agent_result import AgentResult
from .execution_context import ExecutionContext
from .exceptions import StateValidationError, RetryExceededError, AgentExecutionError

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """
    Abstract base class for all AI agents in the ReviewGuard pipeline.
    Provides execution lifecycle, metrics collection, retries, and error handling.
    """
    
    def __init__(
        self, 
        name: str,
        llm_service: Optional[Any] = None, 
        qdrant_service: Optional[Any] = None,
        max_retries: int = 3
    ):
        """
        Initializes the agent with injected dependencies.
        """
        self.name = name
        self.llm_service = llm_service
        self.qdrant_service = qdrant_service
        self.max_retries = max_retries

    def execute(self, state: ReviewState) -> ReviewState:
        """
        Orchestrates the entire agent lifecycle with retry logic and error handling.
        """
        context = ExecutionContext(
            pipeline_id=state.metadata.pipeline_id,
            correlation_id=state.metadata.correlation_id,
            current_agent=self.name,
        )
        
        logger.info(f"[{self.name}] Started execution for pipeline {context.pipeline_id}")
        
        for attempt in range(self.max_retries + 1):
            context.retry_count = attempt
            start_time = time.perf_counter()
            result = AgentResult()
            
            try:
                # 1. Validate State
                self._validate(state)
                
                # 2. Before Execute Hook
                self._before_execute(state, context)
                
                # 3. Process (Abstract)
                result.execution_status = ExecutionStatus.IN_PROGRESS
                state = self._process(state, context)
                
                # If successful, mark result
                result.success = True
                result.execution_status = ExecutionStatus.SUCCESS
                
                # 4. After Execute Hook
                self._after_execute(state, result)
                
                # 5. Metrics Collection
                result.latency_ms = int((time.perf_counter() - start_time) * 1000)
                self._record_metrics(state, result)
                
                logger.info(f"[{self.name}] Completed in {result.latency_ms}ms")
                return state
                
            except StateValidationError as e:
                # State validation errors are fatal and shouldn't be retried
                logger.error(f"[{self.name}] State Validation Failed: {str(e)}")
                result.errors.append(str(e))
                result.execution_status = ExecutionStatus.FAILURE
                self._record_metrics(state, result)
                raise
                
            except Exception as e:
                duration_ms = int((time.perf_counter() - start_time) * 1000)
                logger.warning(f"[{self.name}] Attempt {attempt + 1} failed after {duration_ms}ms: {str(e)}")
                
                if attempt >= self.max_retries:
                    logger.error(f"[{self.name}] Max retries exceeded.")
                    result.errors.append(str(e))
                    result.execution_status = ExecutionStatus.FAILURE
                    self._record_metrics(state, result)
                    raise RetryExceededError(f"Agent {self.name} failed after {self.max_retries} retries.") from e
                    
                # Exponential backoff would go here (e.g. time.sleep(2 ** attempt))

        return state

    def _validate(self, state: ReviewState) -> None:
        """
        Validates the incoming state before execution.
        """
        if not state:
            raise StateValidationError("ReviewState is None.")
        if state.metadata.pipeline_status in (PipelineStatus.CANCELLED, PipelineStatus.FAILED):
            raise StateValidationError(f"Pipeline is in terminal status: {state.metadata.pipeline_status}")
        if not state.metadata.correlation_id:
            raise StateValidationError("Missing correlation_id in state.")

    def _before_execute(self, state: ReviewState, context: ExecutionContext) -> None:
        """
        Protected hook executed immediately before _process.
        Can be overridden by subclasses to setup specific context or logs.
        """
        state.metadata.current_agent = self.name

    @abstractmethod
    def _process(self, state: ReviewState, context: ExecutionContext) -> ReviewState:
        """
        Core logic of the agent. Must be implemented by all subclasses.
        Accepts the current ReviewState and returns the updated ReviewState.
        """
        pass

    def _after_execute(self, state: ReviewState, result: AgentResult) -> None:
        """
        Protected hook executed immediately after a successful _process.
        Can be overridden to clean up or transform outputs.
        """
        pass

    def _record_metrics(self, state: ReviewState, result: AgentResult) -> None:
        """
        Records the telemetry and metrics of the execution into the AuditState.
        """
        state.audit.latency_ms += result.latency_ms
        state.audit.token_usage += result.tokens_used
        state.audit.estimated_cost += result.estimated_cost
        
        if result.errors:
            state.audit.errors.extend([f"[{self.name}] {err}" for err in result.errors])
        if result.warnings:
            state.audit.warnings.extend([f"[{self.name}] {warn}" for warn in result.warnings])
''', encoding="utf-8")

print("Created AI Execution Framework files")
