"""
ReviewGuard AI — Storage Exceptions
Normalized exceptions for the storage layer.
"""

from core.exceptions import ReviewGuardException

class StorageError(ReviewGuardException):
    """Base exception for all storage-related errors."""
    def __init__(self, message: str, error_code: str = "STORAGE_ERROR", http_status: int = 500):
        self.error_code = error_code
        self.http_status = http_status
        super().__init__(message=message)


class FileTooLargeError(StorageError):
    def __init__(self, message: str = "File exceeds the maximum allowed size."):
        super().__init__(message=message, error_code="FILE_TOO_LARGE", http_status=413)


class InvalidMimeTypeError(StorageError):
    def __init__(self, message: str = "Unsupported file type."):
        super().__init__(message=message, error_code="INVALID_FILE_TYPE", http_status=415)


class PathTraversalError(StorageError):
    def __init__(self, message: str = "Invalid filename or path traversal detected."):
        super().__init__(message=message, error_code="PATH_TRAVERSAL_DETECTED", http_status=400)


class FileCorruptedError(StorageError):
    def __init__(self, message: str = "File signature verification failed."):
        super().__init__(message=message, error_code="FILE_CORRUPTED", http_status=422)

class FileNotFoundInStorageError(StorageError):
    def __init__(self, message: str = "File not found in storage provider."):
        super().__init__(message=message, error_code="STORAGE_FILE_NOT_FOUND", http_status=404)
