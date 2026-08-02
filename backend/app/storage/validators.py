"""
ReviewGuard AI — Storage Validators
Enforces strict magic-byte, MIME, and path traversal rules.
"""
import mimetypes
from typing import BinaryIO
from config import settings
from app.storage.exceptions import InvalidMimeTypeError, FileTooLargeError, PathTraversalError

# Pre-defined magic byte signatures for allowed types
MAGIC_BYTES = {
    "application/pdf": b"%PDF-",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": b"PK\x03\x04",
}

def validate_path_safety(filename: str) -> None:
    """Rejects malicious filenames."""
    if "\0" in filename:
        raise PathTraversalError("Null bytes detected in filename.")
    if "/" in filename or "\\" in filename or ".." in filename:
        raise PathTraversalError("Path traversal sequences detected in filename.")

def validate_mime_type(content_type: str, filename: str) -> str:
    """
    Validates that the provided content_type is in our allowed list,
    AND matches the extension of the filename.
    """
    if content_type not in settings.upload_allowed_types:
        raise InvalidMimeTypeError(f"Content type '{content_type}' is not allowed.")
        
    guessed_type, _ = mimetypes.guess_type(filename)
    if guessed_type != content_type:
        # Fallback for weird Windows edge cases where DOCX isn't guessed correctly, 
        # but generally we want strictness.
        if content_type == "text/plain" and filename.endswith(".txt"):
            pass
        elif content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" and filename.endswith(".docx"):
            pass
        else:
            raise InvalidMimeTypeError(f"Extension of '{filename}' does not match content type '{content_type}'.")
            
    return content_type

def validate_magic_bytes(chunk: bytes, expected_mime: str) -> None:
    """
    Inspects the very first chunk of a file to ensure its binary signature 
    matches the expected MIME type.
    """
    if not chunk:
        raise InvalidMimeTypeError("Empty file uploaded.")

    # Text files don't have standard magic bytes, we validate by attempting to decode
    if expected_mime == "text/plain":
        try:
            chunk.decode("utf-8")
            return
        except UnicodeDecodeError:
            raise InvalidMimeTypeError("Text file contains invalid UTF-8 (possible binary).")

    # Binary files must match their known magic signatures
    expected_magic = MAGIC_BYTES.get(expected_mime)
    if not expected_magic:
        raise InvalidMimeTypeError(f"No magic byte validation configured for {expected_mime}")
        
    if not chunk.startswith(expected_magic):
        raise InvalidMimeTypeError(f"File signature (magic bytes) does not match {expected_mime}")
