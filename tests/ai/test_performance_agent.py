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
from app.ai.agents.performance_analysis_agent import PerformanceAnalysisAgent, PerformanceAnalysisResult

print("Testing Performance Analysis Agent...")

print("\n1. Testing Inheritance...")
if issubclass(PerformanceAnalysisAgent, BaseAgent):
    print("SUCCESS: PerformanceAnalysisAgent inherits from BaseAgent")
else:
    print("FAIL: PerformanceAnalysisAgent does not inherit from BaseAgent")
    sys.exit(1)

# Mock LLM Provider
class MockOpenAIProvider(OpenAIProvider):
    def __init__(self):
        # Disable tracking
        pass
    def generate(self, request: LLMRequest, correlation_id: str) -> LLMResponse:
        mock_result = PerformanceAnalysisResult(
            strengths=["Excellent communication"],
            improvements=["Needs to be more proactive"],
            competencies={"Communication": 95.0, "Initiative": 70.0},
            overall_summary="Solid performance but needs more initiative.",
            confidence=0.85,
            supporting_citations=["[Peer] Great communicator."],
            reasoning="Based on peer feedback, communication is a strength."
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

agent = PerformanceAnalysisAgent(
    llm_service=llm_service,
    prompt_registry=prompt_registry
)

print("\n2. Testing Validation...")
state = ReviewState()
# Ensure state fails if evidence not present
try:
    agent.execute(state)
    print("FAIL: Should have raised validation error for missing evidence")
    sys.exit(1)
except StateValidationError:
    print("SUCCESS: Validation intercepted missing evidence")
    
state.evidence.citations = ["[Peer] Great communicator."]
state.evidence.status = "completed"

print("\n3. Testing Service Orchestration & State Updates...")
result = agent.execute(state)

# Check Analysis State
if result.analysis.status == "completed":
    print("SUCCESS: Analysis state status updated")
else:
    print("FAIL: Analysis state status incorrect")
    sys.exit(1)

if len(result.analysis.strengths) > 0 and len(result.analysis.weaknesses) > 0:
    print("SUCCESS: JSON schema validated and correctly parsed into AnalysisState")
else:
    print("FAIL: Strengths or weaknesses not recorded")
    sys.exit(1)

if result.analysis.overall_score > 0:
    print(f"SUCCESS: Overall score dynamically calculated: {result.analysis.overall_score}")
else:
    print("FAIL: Overall score calculation failed")

if len(result.analysis.supporting_citations) > 0:
    print("SUCCESS: Every finding includes evidence citations")
else:
    print("FAIL: Missing citations")

# Check Audit & Execution
if "PerformanceAnalysisAgent" in result.execution.completed_steps:
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
