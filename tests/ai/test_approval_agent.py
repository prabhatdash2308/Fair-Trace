import sys
import logging
import uuid
from typing import Optional, List, Dict, Any
from pathlib import Path
import datetime

# Setup basic logging to catch output
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

from app.ai.state.review_state import ReviewState
from app.ai.base.exceptions import StateValidationError
from app.ai.base.base_agent import BaseAgent

from app.ai.services.llm import LLMService, LLMRequest, LLMResponse, OpenAIProvider, LLMConfig, Telemetry as LLMTelemetry, CircuitBreaker, RetryManager
from app.ai.prompts import PromptRegistry, PromptLoader
from app.ai.agents.human_approval_agent import HumanApprovalAgent, ApprovalPreparationResult

print("Testing Human Approval Agent...")

print("\n1. Testing Inheritance...")
if issubclass(HumanApprovalAgent, BaseAgent):
    print("SUCCESS: HumanApprovalAgent inherits from BaseAgent")
else:
    print("FAIL: HumanApprovalAgent does not inherit from BaseAgent")
    sys.exit(1)

# Mock LLM Provider
class MockOpenAIProvider(OpenAIProvider):
    def __init__(self):
        # Disable tracking
        pass
    def generate(self, request: LLMRequest, correlation_id: str) -> LLMResponse:
        mock_result = ApprovalPreparationResult(
            approval_summary="Ready for manager review.",
            reviewer_checklist=["Verify communication score", "Check missing client feedback"],
            risk_flags=["Missing client feedback"],
            pending_questions=["Does the peer feedback align with your observations?"],
            recommended_action="Proceed to Approval"
        )
        return LLMResponse(
            content=mock_result.model_dump_json(),
            structured_data=mock_result,
            model_used="mock",
            prompt_tokens=10,
            completion_tokens=10,
            cost=0.01
        )

llm_service = LLMService(
    provider=MockOpenAIProvider(),
    config=LLMConfig(),
    telemetry=LLMTelemetry(),
    circuit_breaker=CircuitBreaker(),
    retry_manager=RetryManager()
)

prompt_registry = PromptRegistry(loader=PromptLoader(base_dir=Path("C:/VS CODE/Review Guard AI/Review-Guard-AI/backend/app/ai/prompts")))

agent = HumanApprovalAgent(
    llm_service=llm_service,
    prompt_registry=prompt_registry
)

print("\n2. Testing Validation...")
state = ReviewState()
# Ensure state fails if report not completed
try:
    agent.execute(state)
    print("FAIL: Should have raised validation error for missing report")
    sys.exit(1)
except StateValidationError:
    print("SUCCESS: Validation intercepted missing report")
    
state.report.status = "completed"

print("\n3. Testing Service Orchestration & State Updates...")
result = agent.execute(state)

# Check State
if result.approval.status == "completed":
    print("SUCCESS: Approval state status updated")
else:
    print("FAIL: Approval state status incorrect")
    sys.exit(1)

if len(result.approval.reviewer_checklist) > 0 and len(result.approval.pending_questions) > 0:
    print("SUCCESS: JSON schema validated and correctly parsed into ApprovalState")
else:
    print("FAIL: Approval arrays missing")
    sys.exit(1)

if result.approval.approval_required is True:
    print("SUCCESS: workflow flags generated (approval_required = True)")
else:
    print("FAIL: workflow flags not set")
    sys.exit(1)

if result.approval.approval_status == "PENDING":
    print("SUCCESS: Default status PENDING correctly set")
else:
    print("FAIL: Default status not set")
    sys.exit(1)

if result.approval.submitted_at is not None:
    print("SUCCESS: Timestamp recorded")
else:
    print("FAIL: submitted_at missing")
    sys.exit(1)

# Check Audit & Execution
if "HumanApprovalAgent" in result.execution.completed_steps:
    print("SUCCESS: Execution metrics recorded")
else:
    print("FAIL: Execution state not updated")
    sys.exit(1)

if len(result.audit.agent_logs) > 0:
    print("SUCCESS: AuditState updated with logs and telemetry recorded")
else:
    print("FAIL: AuditState not updated")
    sys.exit(1)

print("\nAll verifications passed!")
