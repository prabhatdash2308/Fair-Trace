"""
Custom exceptions for the AI Execution Framework.
"""

class AgentExecutionError(Exception):
    """Base exception for all agent execution errors."""
    pass

class StateValidationError(AgentExecutionError):
    """Raised when the ReviewState fails validation before execution."""
    pass

class PromptLoadError(AgentExecutionError):
    """Raised when an agent fails to load its required prompt templates."""
    pass

class LLMExecutionError(AgentExecutionError):
    """Raised when the underlying LLM call fails."""
    pass

class RetryExceededError(AgentExecutionError):
    """Raised when an agent exceeds its maximum retry attempts."""
    pass
