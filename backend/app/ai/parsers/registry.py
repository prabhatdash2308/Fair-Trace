from typing import List

from app.ai.parsers.base import BaseParser
from app.ai.parsers.exceptions import UnsupportedDocumentError


class ParserRegistry:
    """
    Maintains a registry of available document parsers.
    Follows the Open/Closed Principle.
    """
    _parsers: List[BaseParser] = []

    @classmethod
    def register(cls, parser: BaseParser) -> None:
        """Register a new parser instance."""
        cls._parsers.append(parser)

    @classmethod
    def get_parser(cls, mime_type: str, extension: str) -> BaseParser:
        """
        Find and return the first registered parser that supports the given type.
        
        Raises:
            UnsupportedDocumentError if no parser is found.
        """
        for parser in cls._parsers:
            if parser.supports(mime_type, extension):
                return parser
                
        raise UnsupportedDocumentError(f"No parser available for mime_type='{mime_type}', extension='{extension}'")

    @classmethod
    def clear(cls) -> None:
        """Clear all registered parsers (useful for testing)."""
        cls._parsers.clear()
