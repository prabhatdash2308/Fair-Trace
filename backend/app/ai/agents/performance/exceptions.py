class PerformanceAgentException(Exception):
    """Base exception for Performance Agent errors."""
    pass

class PromptValidationError(PerformanceAgentException):
    """Raised when prompt rendering fails."""
    pass

class OutputValidationError(PerformanceAgentException):
    """Raised when the LLM output violates business rules or strict schema constraints."""
    pass

class ProviderError(PerformanceAgentException):
    """Raised when the LLM provider fails."""
    pass

class TokenLimitError(PerformanceAgentException):
    """Raised when the input context exceeds maximum allowable tokens."""
    pass

class RetryError(PerformanceAgentException):
    """Raised when the agent fails after exhausting all retries."""
    pass
