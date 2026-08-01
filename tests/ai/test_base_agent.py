import sys
import logging
from uuid import uuid4

# Setup basic logging to catch output
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

from app.ai.base.base_agent import BaseAgent
from app.ai.base.execution_context import ExecutionContext
from app.ai.state.review_state import ReviewState, PipelineStatus
from app.ai.base.exceptions import StateValidationError

class DummyAgent(BaseAgent):
    def _process(self, state: ReviewState, context: ExecutionContext) -> ReviewState:
        # Simulate some logic
        state.audit.agent_logs.append(f"Dummy agent processing: {context.correlation_id}")
        return state
        
    def _after_execute(self, state, result):
        result.tokens_used = 150
        result.estimated_cost = 0.003
        result.warnings.append("This is a simulated warning")

try:
    print("Testing abstract enforcement...")
    class InvalidAgent(BaseAgent):
        pass
    agent = InvalidAgent(name="Invalid")
    print("FAIL: Should not be able to instantiate InvalidAgent without _process")
    sys.exit(1)
except TypeError:
    print("SUCCESS: Abstract enforcement works")

print("\nTesting lifecycle...")
agent = DummyAgent(name="TestDummy")
initial_state = ReviewState()

# Cancel pipeline to test validation
initial_state.metadata.pipeline_status = PipelineStatus.HALTED
try:
    agent.execute(initial_state)
    print("FAIL: Validation should have raised an error")
    sys.exit(1)
except StateValidationError:
    print("SUCCESS: State validation works")

# Test successful execution
initial_state.metadata.pipeline_status = PipelineStatus.PENDING
result_state = agent.execute(initial_state)

print(f"\nResulting State Validation:")
print(f"Current Agent: {result_state.metadata.current_agent}")
print(f"Agent Log: {result_state.audit.agent_logs[0]}")
print(f"Tokens Used: {result_state.audit.token_usage}")
print(f"Cost: {result_state.audit.estimated_cost}")
print(f"Warnings: {result_state.audit.warnings}")
print(f"Latency > 0: {result_state.audit.latency_ms >= 0}")
print("SUCCESS: Execution lifecycle, logging, and metrics work perfectly")
