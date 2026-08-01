"""
Custom exceptions for the Enterprise Vector Store Service.
"""

class VectorStoreError(Exception):
    """Base exception for all Vector Store errors."""
    pass

class CollectionNotFoundError(VectorStoreError):
    """Raised when the requested collection does not exist."""
    pass

class CollectionAlreadyExistsError(VectorStoreError):
    """Raised when trying to create a collection that already exists."""
    pass

class SearchError(VectorStoreError):
    """Raised when a similarity search fails."""
    pass

class UpsertError(VectorStoreError):
    """Raised when upserting vectors fails."""
    pass

class DeleteError(VectorStoreError):
    """Raised when deleting vectors or collections fails."""
    pass

class ConnectionError(VectorStoreError):
    """Raised when connection to the underlying vector store fails."""
    pass
