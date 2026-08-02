class EmbeddingError(Exception):
    """Base exception for all embedding-related errors."""
    pass

class ProviderAuthenticationError(EmbeddingError):
    """Raised when the provider rejects credentials."""
    pass

class RateLimitExceededError(EmbeddingError):
    """Raised when the provider rate limits requests and all retries fail."""
    pass

class InvalidInputError(EmbeddingError):
    """Raised when the batch validation fails before sending to provider."""
    pass

class ProviderTimeoutError(EmbeddingError):
    """Raised when the provider times out."""
    pass
