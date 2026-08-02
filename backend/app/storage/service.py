"""
ReviewGuard AI — Storage Service
Factory and wrapper for the active Storage Provider.
"""
from typing import BinaryIO, Dict, Any
from app.storage.base import StorageProvider
from app.storage.providers.local import LocalStorageProvider

class StorageService:
    """
    Service layer interacting with the configured storage provider.
    Currently hardcoded to LocalStorageProvider, but easily swappable via dependency injection.
    """
    def __init__(self, provider: StorageProvider = None):
        self.provider = provider or LocalStorageProvider()

    @property
    def provider_name(self) -> str:
        return self.provider.provider_name

    async def save(self, stream: BinaryIO, storage_key: str) -> str:
        return await self.provider.save(stream, storage_key)

    async def delete(self, storage_key: str) -> bool:
        return await self.provider.delete(storage_key)

    async def exists(self, storage_key: str) -> bool:
        return await self.provider.exists(storage_key)

    def get_read_stream(self, storage_key: str) -> BinaryIO:
        return self.provider.get_read_stream(storage_key)

    async def get_metadata(self, storage_key: str) -> Dict[str, Any]:
        return await self.provider.get_metadata(storage_key)
