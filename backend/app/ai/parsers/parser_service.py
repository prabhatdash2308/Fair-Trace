import asyncio
import structlog
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select

from config import settings
from models.db.document import Document
from models.enums import ParsingStatus
from app.storage.service import StorageService
from app.storage.exceptions import FileNotFoundInStorageError
from app.ai.parsers.registry import ParserRegistry
from app.ai.parsers.exceptions import ParserError, DocumentTooLargeError
from core.exceptions import NotFoundError, InvalidStateError

logger = structlog.get_logger(__name__)


class DocumentParserService:
    def __init__(self, db: Session, storage_service: Optional[StorageService] = None):
        self.db = db
        self.storage_service = storage_service or StorageService()

    async def parse_document(self, document_id: str, user_id: str) -> dict:
        """
        Orchestrates the entire parsing pipeline for a given document.
        """
        import uuid
        try:
            doc_uuid = uuid.UUID(document_id)
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            raise NotFoundError("Invalid UUID format.")
            
        # 1. Load document
        doc = self.db.scalar(select(Document).where(Document.id == doc_uuid, Document.owner_id == user_uuid))
        if not doc:
            raise NotFoundError("Document not found or access denied.")

        if doc.parsing_status in (ParsingStatus.PARSED, ParsingStatus.PARSING):
            raise InvalidStateError(f"Document is currently {doc.parsing_status.value}.")

        # 2. Transition to PARSING
        doc.parsing_status = ParsingStatus.PARSING
        doc.parsing_error = None
        self.db.commit()
        
        start_time = datetime.now(timezone.utc)
        
        try:
            # Check limits before downloading
            if doc.file_size_bytes > settings.max_file_size_bytes:
                raise DocumentTooLargeError(f"File size {doc.file_size_bytes} exceeds limit {settings.max_file_size_bytes}")

            # 3. Download/Locate file
            try:
                stream = self.storage_service.get_read_stream(doc.storage_key)
            except FileNotFoundInStorageError:
                raise ParserError("File not found in storage layer.")

            file_path = getattr(stream, 'name', None)
            stream.close()
            
            if not file_path:
                raise ParserError("Only local filesystem storage is currently supported for parsing.")

            # 4. Select Parser
            parser = ParserRegistry.get_parser(doc.mime_type, doc.extension)

            # 5. Extract Text (Offload synchronous parsing to thread pool)
            try:
                parsed_doc = await asyncio.wait_for(
                    asyncio.to_thread(parser.parse, file_path),
                    timeout=settings.parser_timeout_seconds
                )
            except asyncio.TimeoutError:
                raise ParserError(f"Parsing timed out after {settings.parser_timeout_seconds} seconds.")

            # 6. Check limits after parsing
            if parsed_doc.page_count > settings.max_pages:
                raise DocumentTooLargeError(f"Page count {parsed_doc.page_count} exceeds limit {settings.max_pages}")
                
            if parsed_doc.character_count > settings.max_text_size_characters:
                raise DocumentTooLargeError(f"Text size {parsed_doc.character_count} exceeds limit {settings.max_text_size_characters}")

            # 7. Update DB
            doc.parsed_text = parsed_doc.text
            doc.page_count = parsed_doc.page_count
            doc.word_count = parsed_doc.word_count
            doc.character_count = parsed_doc.character_count
            doc.parser_used = parsed_doc.parser_used
            doc.parser_version = parsed_doc.parser_version
            doc.parsing_status = ParsingStatus.PARSED
            doc.parsed_at = datetime.now(timezone.utc)
            doc.parse_duration_ms = int((doc.parsed_at - start_time).total_seconds() * 1000)

            self.db.commit()

            # 8. Logging
            logger.info(
                "document_parsed_successfully",
                document_id=str(doc.id),
                user_id=str(user_id),
                parser=doc.parser_used,
                duration_ms=doc.parse_duration_ms,
                pages=doc.page_count,
                words=doc.word_count,
                characters=doc.character_count,
                status=doc.parsing_status.value
            )

            return {
                "status": "parsed",
                "pages": doc.page_count,
                "words": doc.word_count,
                "characters": doc.character_count,
                "parser": doc.parser_used
            }

        except Exception as e:
            self.db.rollback()
            # Reload doc from DB as rollback detaches/reverts it
            doc = self.db.scalar(select(Document).where(Document.id == doc_uuid))
            doc.parsing_status = ParsingStatus.FAILED
            doc.parsing_error = str(e)
            doc.parse_duration_ms = int((datetime.now(timezone.utc) - start_time).total_seconds() * 1000)
            self.db.commit()
            
            logger.error(
                "document_parsing_failed",
                document_id=str(doc.id),
                user_id=str(user_id),
                error=str(e),
                duration_ms=doc.parse_duration_ms,
                status=doc.parsing_status.value
            )
            
            # Rethrow if it's already a domain error, else wrap
            if isinstance(e, ParserError):
                raise e
            raise ParserError(f"Internal parsing error: {str(e)}")
