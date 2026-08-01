import sys
import logging
import uuid
from typing import Optional, List, Dict, Any

# Setup basic logging to catch output
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

from app.ai.state.review_state import ReviewState, BiasType, BiasSeverity, BiasFinding
from app.ai.base.exceptions import StateValidationError
from app.ai.base.base_agent import BaseAgent

from app.ai.services.llm import LLMService, LLMRequest, LLMResponse, OpenAIProvider, LLMConfig, Telemetry as LLMTelemetry, CircuitBreaker, RetryManager
from app.ai.prompts import PromptRegistry, PromptLoader, PromptRenderer
from app.ai.agents.bias_detection_agent import BiasDetectionAgent, BiasDetectionResult

print("Testing Bias Detection Agent...")

print("\\n1. Testing Inheritance...")
if issubclass(BiasDetectionAgent, BaseAgent):
    print("SUCCESS: BiasDetectionAgent inherits from BaseAgent")
else:
    print("FAIL: BiasDetectionAgent does not inherit from BaseAgent")
    sys.exit(1)

# Mock LLM Provider that returns our Pydantic Object directly to bypass actual OpenAI network calls
class MockOpenAIProvider(OpenAIProvider):
    def __init__(self):
        # Disable tracking
        pass
    def generate(self, request: LLMRequest, correlation_id: str) -> LLMResponse:
        mock_result = BiasDetectionResult(
            status="SUCCESS",
            findings=[
                BiasFinding(
                    bias_type=BiasType.RECENCY,
                    severity=BiasSeverity.HIGH,
                    confidence=0.95,
                    reason="Only focused on Q4.",
                    recommendation="Review Q1-Q3.",
                    supporting_citations=["[Peer Feedback] He did well in December."]
                )
            ]
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

from pathlib import Path
prompt_registry = PromptRegistry(loader=PromptLoader(base_dir=Path("C:/VS CODE/Review Guard AI/Review-Guard-AI/backend/app/ai/prompts")))

agent = BiasDetectionAgent(
    llm_service=llm_service,
    prompt_registry=prompt_registry
)

print("\n2. Testing Validation...")
state = ReviewState()
# Ensure state fails if evidence not completed
try:
    agent.execute(state)
    print("FAIL: Should have raised validation error for incomplete evidence")
    sys.exit(1)
except StateValidationError:
    print("SUCCESS: Validation intercepted incomplete evidence")
    
state.evidence.status = "completed"
state.evidence.citations = ["[Peer Feedback] He did well in December."]

print("\n3. Testing Service Orchestration & State Updates...")
result = agent.execute(state)

# Check Bias State
if result.bias.status == "completed":
    print("SUCCESS: Bias state status updated")
else:
    print("FAIL: Bias state status incorrect")
    sys.exit(1)

if len(result.bias.findings) > 0:
    print(f"SUCCESS: Bias findings recorded: {len(result.bias.findings)}")
else:
    print("FAIL: Findings not recorded")
    sys.exit(1)

if result.bias.findings[0].bias_type == BiasType.RECENCY:
    print("SUCCESS: JSON schema validated and correctly parsed into enums")
else:
    print("FAIL: Enum parsing failed")

if len(result.bias.findings[0].supporting_citations) > 0:
    print("SUCCESS: Every finding includes evidence citations")
else:
    print("FAIL: Missing citations")

# Check Audit & Execution
if "BiasDetectionAgent" in result.execution.completed_steps:
    print("SUCCESS: Execution metrics recorded")
else:
    print("FAIL: Execution state not updated")
    sys.exit(1)

if len(result.audit.agent_logs) > 0:
    print("SUCCESS: AuditState updated with logs")
else:
    print("FAIL: AuditState not updated")
    sys.exit(1)

print("\nAll verifications passed!")
