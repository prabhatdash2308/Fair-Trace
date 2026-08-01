"""
Custom exceptions for the Enterprise LLM Service.
"""

class LLMException(Exception):
    """Base exception for all LLM service errors."""
    pass

class ProviderError(LLMException):
    """Raised when the underlying LLM provider fails."""
    pass

class RateLimitError(ProviderError):
    """Raised when hitting rate limits."""
    pass

class ContextLengthExceededError(ProviderError):
    """Raised when the prompt exceeds the model's maximum context length."""
    pass

class LLMValidationError(LLMException):
    """Raised when the LLM response fails schema validation."""
    pass

class CircuitBreakerOpenError(LLMException):
    """Raised when the circuit breaker prevents a request."""
    pass
