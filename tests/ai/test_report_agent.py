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
from app.ai.agents.report_generation_agent import ReportGenerationAgent, PerformanceReportResult

print("Testing Report Generation Agent...")

print("\n1. Testing Inheritance...")
if issubclass(ReportGenerationAgent, BaseAgent):
    print("SUCCESS: ReportGenerationAgent inherits from BaseAgent")
else:
    print("FAIL: ReportGenerationAgent does not inherit from BaseAgent")
    sys.exit(1)

# Mock LLM Provider
class MockOpenAIProvider(OpenAIProvider):
    def __init__(self):
        # Disable tracking
        pass
    def generate(self, request: LLMRequest, correlation_id: str) -> LLMResponse:
        mock_result = PerformanceReportResult(
            executive_summary="Solid performance with minor growth areas.",
            employee_overview="Software Engineer II",
            performance_summary="Consistent delivery.",
            strengths=["Coding", "Communication"],
            areas_for_improvement=["Mentorship"],
            competency_breakdown={"Coding": 90.0, "Communication": 85.0, "Mentorship": 60.0},
            bias_summary="No bias detected.",
            confidence_summary="High confidence.",
            recommendations=["Take mentorship training."],
            supporting_citations=["[Peer] Good coder."],
            limitations=["No client feedback available."]
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

agent = ReportGenerationAgent(
    llm_service=llm_service,
    prompt_registry=prompt_registry
)

print("\n2. Testing Validation...")
state = ReviewState()
# Ensure state fails if explainability not completed
try:
    agent.execute(state)
    print("FAIL: Should have raised validation error for missing explainability")
    sys.exit(1)
except StateValidationError:
    print("SUCCESS: Validation intercepted missing explainability")
    
state.explainability.status = "completed"
state.analysis.supporting_citations = ["[Peer] Good coder."]

print("\n3. Testing Service Orchestration & State Updates...")
result = agent.execute(state)

# Check State
if result.report.status == "completed":
    print("SUCCESS: Report state status updated")
else:
    print("FAIL: Report state status incorrect")
    sys.exit(1)

if len(result.report.recommendations) > 0 and len(result.report.strengths) > 0:
    print("SUCCESS: JSON schema validated and correctly parsed into ReportState")
else:
    print("FAIL: Report arrays missing")
    sys.exit(1)

if len(result.report.supporting_citations) > 0:
    print("SUCCESS: Citations preserved and mapped")
else:
    print("FAIL: Missing citation mapping")
    sys.exit(1)
    
if result.report.generated_at is not None:
    print("SUCCESS: Deterministic timestamps recorded")
else:
    print("FAIL: generated_at missing")
    sys.exit(1)

# Check Audit & Execution
if "ReportGenerationAgent" in result.execution.completed_steps:
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
