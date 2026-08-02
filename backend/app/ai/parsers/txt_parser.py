from charset_normalizer import from_path, __version__ as charset_version
from typing import Dict, Any

from app.ai.parsers.base import BaseParser
from app.ai.parsers.models import ParsedDocument
from app.ai.parsers.exceptions import NoTextFoundError, ParsingFailedError
from app.ai.parsers.text_normalizer import TextNormalizer


class TXTParser(BaseParser):
    @property
    def parser_name(self) -> str:
        return "charset-normalizer"

    @property
    def parser_version(self) -> str:
        return charset_version

    def supports(self, mime_type: str, extension: str) -> bool:
        return mime_type == "text/plain" or extension.lower() == ".txt"

    def parse(self, file_path: str) -> ParsedDocument:
        try:
            # Auto-detect encoding and load text
            results = from_path(file_path)
            best_match = results.best()
            
            if best_match is None:
                raise ParsingFailedError("Could not determine text encoding.")
                
            raw_text = str(best_match)
            normalized_text = TextNormalizer.normalize(raw_text)
            
            if not normalized_text:
                raise NoTextFoundError("No text could be extracted from the TXT document.")
            
            word_count = len(normalized_text.split())
            estimated_pages = max(1, word_count // 250)
            
            return ParsedDocument(
                text=normalized_text,
                page_count=estimated_pages,
                word_count=word_count,
                character_count=len(normalized_text),
                title=None,
                author=None,
                metadata={"encoding": best_match.encoding},
                parser_used=self.parser_name,
                parser_version=self.parser_version,
            )
            
        except NoTextFoundError:
            raise
        except Exception as e:
            raise ParsingFailedError(f"Failed to parse TXT: {str(e)}") from e
