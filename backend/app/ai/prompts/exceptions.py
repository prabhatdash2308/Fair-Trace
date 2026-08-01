"""
Custom exceptions for the Prompt Management System.
"""

class PromptException(Exception):
    """Base exception for all prompt-related errors."""
    pass

class PromptNotFoundError(PromptException):
    """Raised when a prompt file or registered prompt is not found."""
    pass

class PromptValidationError(PromptException):
    """Raised when prompt rendering fails validation (missing/unused variables)."""
    pass

class PromptRenderError(PromptException):
    """Raised when rendering a prompt fails unexpectedly."""
    pass

class PromptRegistrationError(PromptException):
    """Raised when there is an issue registering a prompt (e.g., duplicate)."""
    pass
