class VectorStoreError(Exception):
    """Base exception for all vector store errors."""
    pass

class VectorCollectionError(VectorStoreError):
    """Raised when there is an issue with the Qdrant collection."""
    pass

class VectorUpsertError(VectorStoreError):
    """Raised when an upsert operation fails (validation or network)."""
    pass

class VectorValidationError(VectorStoreError):
    """Raised when a vector violates constraints (length, NaN, etc.)."""
    pass
