"""
Custom exceptions for the Enterprise Embedding Service.
"""

class EmbeddingException(Exception):
    """Base exception for all Embedding service errors."""
    pass

class EmbeddingProviderError(EmbeddingException):
    """Raised when the underlying embedding provider fails."""
    pass

class ChunkingError(EmbeddingException):
    """Raised when text chunking fails (e.g., invalid parameters)."""
    pass

class EmbeddingCacheError(EmbeddingException):
    """Raised when cache operations fail."""
    pass
