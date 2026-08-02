import pypdf
from typing import Dict, Any

from app.ai.parsers.base import BaseParser
from app.ai.parsers.models import ParsedDocument
from app.ai.parsers.exceptions import EncryptedDocumentError, NoTextFoundError, ParsingFailedError
from app.ai.parsers.text_normalizer import TextNormalizer


class PDFParser(BaseParser):
    @property
    def parser_name(self) -> str:
        return "pypdf"

    @property
    def parser_version(self) -> str:
        return pypdf.__version__

    def supports(self, mime_type: str, extension: str) -> bool:
        return mime_type == "application/pdf" or extension.lower() == ".pdf"

    def parse(self, file_path: str) -> ParsedDocument:
        try:
            reader = pypdf.PdfReader(file_path)
            
            if reader.is_encrypted:
                raise EncryptedDocumentError("PDF is encrypted or password-protected.")
                
            text_chunks = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_chunks.append(page_text)
                    
            raw_text = "\n\n".join(text_chunks)
            normalized_text = TextNormalizer.normalize(raw_text)
            
            if not normalized_text:
                raise NoTextFoundError("No text could be extracted from the PDF.")
                
            metadata = self._extract_metadata(reader)
            
            return ParsedDocument(
                text=normalized_text,
                page_count=len(reader.pages),
                word_count=len(normalized_text.split()),
                character_count=len(normalized_text),
                title=metadata.get("title"),
                author=metadata.get("author"),
                metadata=metadata,
                parser_used=self.parser_name,
                parser_version=self.parser_version,
            )
            
        except (EncryptedDocumentError, NoTextFoundError):
            raise
        except Exception as e:
            raise ParsingFailedError(f"Failed to parse PDF: {str(e)}") from e

    def _extract_metadata(self, reader: pypdf.PdfReader) -> Dict[str, Any]:
        result = {}
        if reader.metadata:
            for key, value in reader.metadata.items():
                clean_key = key.strip('/').lower()
                result[clean_key] = str(value) if value else None
                
        # Remap standard keys if present
        if "title" in result:
            result["title"] = result.pop("title")
        if "author" in result:
            result["author"] = result.pop("author")
            
        return result
