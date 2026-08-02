from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

from app.ai.parsers.models import ParsedDocument


class BaseParser(ABC):
    """
    Abstract base class for all document parsers.
    Parsers are responsible for extracting text and metadata from raw file contents.
    """

    @property
    @abstractmethod
    def parser_name(self) -> str:
        """Name of the parser (e.g., 'pypdf')."""
        pass

    @property
    @abstractmethod
    def parser_version(self) -> str:
        """Version of the underlying parsing library."""
        pass

    @abstractmethod
    def supports(self, mime_type: str, extension: str) -> bool:
        """Check if this parser supports the given document type."""
        pass

    @abstractmethod
    def parse(self, file_path: str) -> ParsedDocument:
        """
        Parse the document at the given file path.
        
        Args:
            file_path: Absolute path to the file on disk.
            
        Returns:
            ParsedDocument containing text, metadata, and statistics.
            
        Raises:
            ParserError (and subclasses) on parsing failures.
        """
        pass
