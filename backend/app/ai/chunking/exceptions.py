from core.exceptions import FairTraceException

class ChunkingError(FairTraceException):
    """Base exception for all chunking-related errors."""
    def __init__(self, message: str, error_code: str = "CHUNKING_ERROR", http_status: int = 500):
        self.error_code = error_code
        self.http_status = http_status
        super().__init__(message=message)

class OversizedChunkError(ChunkingError):
    def __init__(self, message: str = "Chunk exceeds maximum allowed token or character size."):
        super().__init__(message=message, error_code="OVERSIZED_CHUNK", http_status=422)

class DuplicateChunkError(ChunkingError):
    def __init__(self, message: str = "Duplicate chunk detected based on checksum."):
        super().__init__(message=message, error_code="DUPLICATE_CHUNK", http_status=422)

class ValidationFailedError(ChunkingError):
    def __init__(self, message: str = "Chunk validation failed (e.g., empty, overlap invalid)."):
        super().__init__(message=message, error_code="VALIDATION_FAILED", http_status=422)
