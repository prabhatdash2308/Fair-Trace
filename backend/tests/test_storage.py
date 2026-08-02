import pytest
import io
import uuid
from unittest.mock import patch, MagicMock

from app.storage.validators import validate_path_safety, validate_mime_type, validate_magic_bytes
from app.storage.exceptions import PathTraversalError, InvalidMimeTypeError
from config import settings

def test_validate_path_safety():
    # Valid
    validate_path_safety("safe_file.pdf")
    validate_path_safety("unicode_文件.docx")
    
    # Path traversal attempts
    with pytest.raises(PathTraversalError):
        validate_path_safety("../etc/passwd")
    with pytest.raises(PathTraversalError):
        validate_path_safety("..\\windows\\system32")
    with pytest.raises(PathTraversalError):
        validate_path_safety("safe_file.pdf\0.exe")

def test_validate_mime_type():
    # Valid
    assert validate_mime_type("application/pdf", "test.pdf") == "application/pdf"
    assert validate_mime_type("text/plain", "test.txt") == "text/plain"
    
    # Invalid extension
    with pytest.raises(InvalidMimeTypeError):
        validate_mime_type("application/pdf", "test.docx")
        
    # Unallowed content type
    with pytest.raises(InvalidMimeTypeError):
        validate_mime_type("application/json", "test.json")

def test_validate_magic_bytes():
    # Valid PDF
    validate_magic_bytes(b"%PDF-1.4\n...", "application/pdf")
    
    # Valid DOCX
    validate_magic_bytes(b"PK\x03\x04...", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    
    # Valid TXT
    validate_magic_bytes(b"Hello world", "text/plain")
    
    # Invalid TXT (binary payload)
    with pytest.raises(InvalidMimeTypeError):
        validate_magic_bytes(b"\x89PNG\r\n\x1a\n", "text/plain")
        
    # Spoofed PDF (PNG magic bytes)
    with pytest.raises(InvalidMimeTypeError):
        validate_magic_bytes(b"\x89PNG\r\n\x1a\n", "application/pdf")
        
    # Empty file
    with pytest.raises(InvalidMimeTypeError):
        validate_magic_bytes(b"", "application/pdf")
