import sys
import logging
from typing import Optional, List, Dict, Any
from pathlib import Path
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
from app.ai.state.review_state import ReviewState, PipelineStatus
from app.ai.base.exceptions import StateValidationError, RetryExceededError
from app.ai.base.base_agent import BaseAgent
from app.ai.base.execution_context import ExecutionContext
from app.ai.graph.graph import ReviewGuardGraph

print("Testing Enterprise LangGraph Orchestration...")
class MockAgent(BaseAgent):
    def __init__(self, name):
        super().__init__(name=name, max_retries=1)
    def _validate_before_process(self, state: ReviewState) -> None:
        pass
    def _process(self, state: ReviewState, context: ExecutionContext) -> ReviewState:
        state.execution.completed_steps.append(self.name)
        if self.name == "approval":
            state.approval.approval_status = "PENDING"
        return state

class FailingAgent(BaseAgent):
    def __init__(self, name):
        super().__init__(name=name, max_retries=1)
    def _validate_before_process(self, state: ReviewState) -> None:
        pass
    def _process(self, state: ReviewState, context: ExecutionContext) -> ReviewState:
        raise RetryExceededError("Simulated LLM failure")

intake = MockAgent("intake")
embedding = MockAgent("embedding")
retrieval = MockAgent("retrieval")
bias = MockAgent("bias")
analysis = MockAgent("analysis")
explainability = MockAgent("explainability")
report = MockAgent("report")
approval = MockAgent("approval")
finalization = MockAgent("finalization")

graph = ReviewGuardGraph(intake, embedding, retrieval, bias, analysis, explainability, report, approval, finalization)

state = ReviewState()
state.metadata.pipeline_status = PipelineStatus.RUNNING
result_state = graph.invoke(state, thread_id="test_1")
if "approval" in result_state.execution.completed_steps and "finalization" not in result_state.execution.completed_steps:
    print("SUCCESS: approval interrupt works")
else:
    print("FAIL: interrupt failed", result_state.execution.completed_steps)
    sys.exit(1)

# Update state in memory
result_state.approval.approval_status = "APPROVED"
graph.executor.compiled_graph.update_state({"configurable": {"thread_id": "test_1"}}, result_state)
result_state = graph.invoke(None, thread_id="test_1")

if "finalization" in result_state.execution.completed_steps:
    print("SUCCESS: finalization path works")
else:
    print("FAIL: finalization path failed", result_state.execution.completed_steps)
    sys.exit(1)

state2 = ReviewState()
state2.metadata.pipeline_status = PipelineStatus.RUNNING
result2 = graph.invoke(state2, thread_id="test_reject")
result2.approval.approval_status = "REJECTED"
graph.executor.compiled_graph.update_state({"configurable": {"thread_id": "test_reject"}}, result2)
result2 = graph.invoke(None, thread_id="test_reject")
if "finalization" not in result2.execution.completed_steps:
    print("SUCCESS: rejected path works")
else:
    print("FAIL: rejected path failed")
    sys.exit(1)

state3 = ReviewState()
state3.metadata.pipeline_status = PipelineStatus.RUNNING
events = list(graph.stream(state3, thread_id="test_stream"))
if len(events) > 0:
    print("SUCCESS: stream() works")
else:
    print("FAIL: stream() failed")
    sys.exit(1)

graph_fail = ReviewGuardGraph(intake, embedding, retrieval, bias, FailingAgent("analysis"), explainability, report, approval, finalization)
state4 = ReviewState()
state4.metadata.pipeline_status = PipelineStatus.RUNNING
result4 = graph_fail.invoke(state4, thread_id="test_fail")
if result4.metadata.pipeline_status == PipelineStatus.FAILED and result4.execution.retry_count >= 3:
    print("SUCCESS: retry works and fails properly after counts exceeded")
else:
    print("FAIL: retry mechanism didn't behave correctly", result4.metadata.pipeline_status, result4.execution.retry_count)
    sys.exit(1)

print("\nAll LangGraph verifications passed!")
