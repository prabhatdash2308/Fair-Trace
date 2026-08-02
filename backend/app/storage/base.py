"""
ReviewGuard AI — Storage Provider Base Interface
Defines the contract for all storage providers (Local, S3, Azure, etc.)
"""
from abc import ABC, abstractmethod
from typing import BinaryIO, Dict, Any


class StorageProvider(ABC):
    """
    Abstract Base Class for Enterprise Storage Providers.
    All implementations must guarantee atomic saves and proper error handling.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Returns the unique name of the provider (e.g., 'local', 's3')"""
        pass

    @abstractmethod
    async def save(self, stream: BinaryIO, storage_key: str) -> str:
        """
        Saves a byte stream to the underlying storage.
        Must handle its own directory/bucket creation if needed.
        
        Args:
            stream: The file-like object to read from.
            storage_key: The designated storage key (e.g., '2026/07/31/uuid.pdf').
            
        Returns:
            The fully qualified path or URI (useful for logging, NEVER returned to client).
        """
        pass

    @abstractmethod
    async def delete(self, storage_key: str) -> bool:
        """
        Deletes a file from storage.
        
        Args:
            storage_key: The storage key.
            
        Returns:
            True if deleted, False if it did not exist.
        """
        pass

    @abstractmethod
    async def exists(self, storage_key: str) -> bool:
        """Checks if a file exists in storage."""
        pass

    @abstractmethod
    def get_read_stream(self, storage_key: str) -> BinaryIO:
        """
        Returns a readable stream for the file.
        Must be closed by the caller.
        """
        pass

    @abstractmethod
    async def get_metadata(self, storage_key: str) -> Dict[str, Any]:
        """
        Retrieves provider-specific metadata (size, created timestamp, etc).
        """
        pass
