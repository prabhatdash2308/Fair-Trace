"""
ReviewGuard AI — Parser Exceptions
"""

from core.exceptions import FairTraceException

class ParserError(FairTraceException):
    """Base exception for all parsing-related errors."""
    def __init__(self, message: str, error_code: str = "PARSER_ERROR", http_status: int = 500):
        self.error_code = error_code
        self.http_status = http_status
        super().__init__(message=message)


class UnsupportedDocumentError(ParserError):
    def __init__(self, message: str = "Document type is not supported by any registered parser."):
        super().__init__(message=message, error_code="UNSUPPORTED_DOCUMENT", http_status=415)


class EncryptedDocumentError(ParserError):
    def __init__(self, message: str = "Document is encrypted or password protected."):
        super().__init__(message=message, error_code="ENCRYPTED_DOCUMENT", http_status=422)


class NoTextFoundError(ParserError):
    def __init__(self, message: str = "No readable text was found in the document (possibly image-only)."):
        super().__init__(message=message, error_code="NO_TEXT_FOUND", http_status=422)


class ParsingFailedError(ParserError):
    def __init__(self, message: str = "Failed to parse the document."):
        super().__init__(message=message, error_code="PARSING_FAILED", http_status=422)


class DocumentTooLargeError(ParserError):
    def __init__(self, message: str = "Document exceeds parsing limits."):
        super().__init__(message=message, error_code="DOCUMENT_TOO_LARGE", http_status=413)
