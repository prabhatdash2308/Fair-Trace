class BiasAgentException(Exception):
    """Base exception for Bias Agent errors."""
    pass

class OutputValidationError(BiasAgentException):
    """Raised when the LLM output violates business rules or strict schema constraints."""
    pass

class TokenLimitError(BiasAgentException):
    """Raised when the input context exceeds maximum allowable tokens."""
    pass
