class RetrievalError(Exception):
    """Base class for retrieval exceptions."""
    pass

class ContextLimitError(RetrievalError):
    """Raised when context token limit is exceeded."""
    pass

class InvalidPayloadError(RetrievalError):
    """Raised when retrieved payload is invalid or incomplete."""
    pass
