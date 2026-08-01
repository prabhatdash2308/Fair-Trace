import sys
import logging
from pydantic import BaseModel

# Setup basic logging to catch output
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

from backend.app.ai.services.llm import (
    LLMService,
    OpenAIProvider,
    LLMConfig,
    CircuitBreaker,
    RetryManager,
    Telemetry,
    LLMRequest,
    TokenCounter,
    CostCalculator,
    LLMValidationError,
    CircuitBreakerOpenError
)

print("Testing Enterprise LLM Service...")

config = LLMConfig()
provider = OpenAIProvider()
circuit_breaker = CircuitBreaker(failure_threshold=2)
retry_manager = RetryManager()
telemetry = Telemetry()

service = LLMService(
    provider=provider,
    config=config,
    circuit_breaker=circuit_breaker,
    retry_manager=retry_manager,
    telemetry=telemetry
)

print("\n1. Testing Provider Abstraction & Telemetry...")
req1 = LLMRequest(system_prompt="sys", user_prompt="user")
res1 = service.generate(req1, correlation_id="req-1")

print(f"SUCCESS: LLMService generated response: '{res1.content}'")
if telemetry.total_requests == 1:
    print("SUCCESS: Telemetry recorded request.")
else:
    print("FAIL: Telemetry missed request.")
    sys.exit(1)

print("\n2. Testing Token Counting & Cost Calculator...")
tokens = TokenCounter.count_tokens("This is a test of the token counter.", "gpt-4o")
print(f"Token Count: {tokens}")
cost = CostCalculator.calculate("gpt-4o", 1000, 1000)
print(f"Cost for 1k/1k: ")
if cost == 0.020:
    print("SUCCESS: Cost calculated correctly (0.005 + 0.015)")
else:
    print("FAIL: Cost miscalculated")

print("\n3. Testing Response Validation (Structured Output)...")
class TestSchema(BaseModel):
    status: str
    score: int

req2 = LLMRequest(system_prompt="sys", user_prompt="user", response_format=TestSchema)
res2 = service.generate(req2, correlation_id="req-2")

if isinstance(res2.structured_data, TestSchema):
    print("SUCCESS: Response validation parsed structured output to Pydantic Model")
else:
    print("FAIL: Structured output is missing or incorrect type")
    sys.exit(1)

print("\n4. Testing Circuit Breaker & Retry...")
# We will inject a dummy provider that always fails to test the circuit breaker
class FailingProvider(OpenAIProvider):
    def generate(self, req, conf):
        raise ValueError("Simulated Provider Failure")

failing_service = LLMService(
    provider=FailingProvider(),
    config=config,
    circuit_breaker=circuit_breaker,
    retry_manager=retry_manager,
    telemetry=telemetry
)

try:
    failing_service.generate(req1, correlation_id="req-fail-1")
    print("FAIL: Exception should have been thrown")
    sys.exit(1)
except ValueError:
    print("SUCCESS: Error correctly bubbled up")

try:
    failing_service.generate(req1, correlation_id="req-fail-2")
except ValueError:
    pass
    
# Third time should hit CircuitBreakerOpenError because failure_threshold=2
try:
    failing_service.generate(req1, correlation_id="req-fail-3")
    print("FAIL: Circuit Breaker should be open")
    sys.exit(1)
except CircuitBreakerOpenError:
    print("SUCCESS: Circuit Breaker triggered successfully")

print("\nAll verifications passed!")
