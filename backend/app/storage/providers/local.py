"""
ReviewGuard AI — Local Storage Provider
Implements the StorageProvider interface for local filesystem sharding.
"""
import os
import aiofiles
from typing import BinaryIO, Dict, Any

from config import settings
from app.storage.base import StorageProvider
from app.storage.exceptions import StorageError, FileNotFoundInStorageError


class LocalStorageProvider(StorageProvider):
    """
    Persists files locally inside UPLOAD_DIRECTORY.
    Assumes `storage_key` dictates the relative subpath structure (e.g., YYYY/MM/DD/uuid.pdf).
    """

    @property
    def provider_name(self) -> str:
        return "local"

    def _get_absolute_path(self, storage_key: str) -> str:
        """Resolves the storage key to an absolute OS path, preventing traversal."""
        # Clean the key to prevent traversal
        clean_key = storage_key.lstrip("/")
        abs_path = os.path.abspath(os.path.join(settings.upload_directory, clean_key))
        
        if not abs_path.startswith(os.path.abspath(settings.upload_directory)):
            raise StorageError("Path traversal attempt detected in storage key.")
            
        return abs_path

    async def save(self, stream: BinaryIO, storage_key: str) -> str:
        abs_path = self._get_absolute_path(storage_key)
        
        # Ensure directory shards exist
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)

        try:
            # For LocalStorage, we expect the stream to be an opened file or BytesIO
            # We will read chunks and write to aiofiles
            async with aiofiles.open(abs_path, 'wb') as out_file:
                while True:
                    chunk = stream.read(8192)
                    if not chunk:
                        break
                    await out_file.write(chunk)
                    
            return abs_path
        except Exception as e:
            raise StorageError(f"Failed to save file to local storage: {str(e)}")

    async def delete(self, storage_key: str) -> bool:
        abs_path = self._get_absolute_path(storage_key)
        if os.path.exists(abs_path):
            try:
                os.remove(abs_path)
                return True
            except Exception as e:
                raise StorageError(f"Failed to delete file from local storage: {str(e)}")
        return False

    async def exists(self, storage_key: str) -> bool:
        return os.path.exists(self._get_absolute_path(storage_key))

    def get_read_stream(self, storage_key: str) -> BinaryIO:
        abs_path = self._get_absolute_path(storage_key)
        if not os.path.exists(abs_path):
            raise FileNotFoundInStorageError()
        return open(abs_path, "rb")

    async def get_metadata(self, storage_key: str) -> Dict[str, Any]:
        abs_path = self._get_absolute_path(storage_key)
        if not os.path.exists(abs_path):
            raise FileNotFoundInStorageError()
            
        stat = os.stat(abs_path)
        return {
            "size": stat.st_size,
            "created_at": stat.st_ctime,
            "modified_at": stat.st_mtime,
        }
