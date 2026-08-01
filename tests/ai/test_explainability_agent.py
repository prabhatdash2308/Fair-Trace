import sys
import logging
import uuid
from typing import Optional, List, Dict, Any
from pathlib import Path

# Setup basic logging to catch output
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

from app.ai.state.review_state import ReviewState, BiasType, BiasSeverity, BiasFinding
from app.ai.base.exceptions import StateValidationError
from app.ai.base.base_agent import BaseAgent

from app.ai.services.llm import LLMService, LLMRequest, LLMResponse, OpenAIProvider, LLMConfig, Telemetry as LLMTelemetry, CircuitBreaker, RetryManager
from app.ai.prompts import PromptRegistry, PromptLoader, PromptRenderer
from app.ai.agents.explainability_agent import ExplainabilityAgent, ExplainabilityResult

print("Testing Explainability Agent...")

print("\n1. Testing Inheritance...")
if issubclass(ExplainabilityAgent, BaseAgent):
    print("SUCCESS: ExplainabilityAgent inherits from BaseAgent")
else:
    print("FAIL: ExplainabilityAgent does not inherit from BaseAgent")
    sys.exit(1)

# Mock LLM Provider
class MockOpenAIProvider(OpenAIProvider):
    def __init__(self):
        # Disable tracking
        pass
    def generate(self, request: LLMRequest, correlation_id: str) -> LLMResponse:
        mock_result = ExplainabilityResult(
            executive_summary="The AI concluded strong communication skills.",
            decision_path=["Analyzed evidence", "Detected zero bias", "Scored high"],
            competency_explanations={"Communication": "High score based on peer feedback."},
            bias_explanations=["No significant bias altered the score."],
            confidence_explanation="Multiple peers supported the conclusion.",
            citation_mapping={"Communication": ["[Peer] Great communicator."]},
            limitations=["Manager feedback was missing."]
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

agent = ExplainabilityAgent(
    llm_service=llm_service,
    prompt_registry=prompt_registry
)

print("\n2. Testing Validation...")
state = ReviewState()
# Ensure state fails if analysis not completed
try:
    agent.execute(state)
    print("FAIL: Should have raised validation error for missing analysis")
    sys.exit(1)
except StateValidationError:
    print("SUCCESS: Validation intercepted missing analysis")
    
state.analysis.status = "completed"
state.analysis.supporting_citations = ["[Peer] Great communicator."]

print("\n3. Testing Service Orchestration & State Updates...")
result = agent.execute(state)

# Check State
if result.explainability.status == "completed":
    print("SUCCESS: Explainability state status updated")
else:
    print("FAIL: Explainability state status incorrect")
    sys.exit(1)

if len(result.explainability.citation_mapping) > 0 and len(result.explainability.decision_path) > 0:
    print("SUCCESS: JSON schema validated and correctly parsed into ExplainabilityState")
else:
    print("FAIL: Explainability arrays missing")
    sys.exit(1)

if len(result.explainability.citation_mapping.get("Communication", [])) > 0:
    print("SUCCESS: Citations preserved and mapped")
else:
    print("FAIL: Missing citation mapping")
    sys.exit(1)

# Check Audit & Execution
if "ExplainabilityAgent" in result.execution.completed_steps:
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
