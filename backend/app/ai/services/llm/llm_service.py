"""
The orchestrator of the Enterprise LLM Service.
"""
import time
from .config import LLMConfig
from .models import LLMRequest, LLMResponse
from .providers import LLMProvider
from .circuit_breaker import CircuitBreaker
from .retry import RetryManager
from .telemetry import Telemetry
from .cost_calculator import CostCalculator
from .token_counter import TokenCounter
from .response_validator import ResponseValidator
from .exceptions import ProviderError

class LLMService:
    """
    Enterprise LLM Service Gateway.
    No agent should bypass this service.
    """
    def __init__(
        self,
        provider: LLMProvider,
        config: LLMConfig,
        circuit_breaker: CircuitBreaker,
        retry_manager: RetryManager,
        telemetry: Telemetry
    ):
        self.provider = provider
        self.config = config
        self.circuit_breaker = circuit_breaker
        self.retry_manager = retry_manager
        self.telemetry = telemetry
        
    def generate(self, request: LLMRequest, correlation_id: str) -> LLMResponse:
        """
        Executes a prompt through the LLM pipeline with full observability, retries, and circuit breaking.
        """
        self.circuit_breaker.check_allowed()
        
        start_time = time.perf_counter()
        
        try:
            def execute_call():
                return self.provider.generate(request, self.config)
                
            # Execute with Retry
            response = self.retry_manager.execute(execute_call, correlation_id)
            
            # Validation for Structured Output
            if request.response_format:
                response.structured_data = ResponseValidator.parse_and_validate(response, request.response_format)
                
            # Telemetry & Cost
            latency_ms = int((time.perf_counter() - start_time) * 1000)
            cost = CostCalculator.calculate(response.model_used, response.prompt_tokens, response.completion_tokens)
            
            self.telemetry.record_request(
                correlation_id=correlation_id,
                model=response.model_used,
                latency_ms=latency_ms,
                tokens=response.total_tokens,
                cost=cost
            )
            
            self.circuit_breaker.record_success()
            return response
            
        except Exception as e:
            self.circuit_breaker.record_failure()
            self.telemetry.record_error(correlation_id, e)
            raise
