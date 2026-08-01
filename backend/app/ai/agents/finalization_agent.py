"""
Finalization Agent for finalizing the review pipeline state.
"""
import time
import datetime
from app.ai.base.base_agent import BaseAgent
from app.ai.base.execution_context import ExecutionContext
from app.ai.state.review_state import ReviewState, PipelineStatus
from app.ai.base.exceptions import StateValidationError

class FinalizationAgent(BaseAgent):
    def __init__(self, name="FinalizationAgent", max_retries=1):
        super().__init__(name=name, max_retries=max_retries)

    def _validate_before_process(self, state: ReviewState) -> None:
        if state.approval.approval_status != "APPROVED":
            raise StateValidationError("Cannot finalize unless approved.")

    def _process(self, state: ReviewState, context: ExecutionContext) -> ReviewState:
        self._validate_before_process(state)
        
        start_time = time.perf_counter()
        
        state.metadata.pipeline_status = PipelineStatus.COMPLETED
        state.report.status = "finalized"
        
        latency = int((time.perf_counter() - start_time) * 1000)
        state.execution.completed_steps.append(self.name)
        state.audit.agent_logs.append(f"[{self.name}] Pipeline Finalized in {latency}ms.")
        return state
