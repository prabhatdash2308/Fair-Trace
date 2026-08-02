import pytest
import asyncio
import tempfile
import os
import base64
from unittest.mock import MagicMock
from uuid import uuid4

from app.ai.parsers.parser_service import DocumentParserService
from app.ai.parsers.exceptions import ParserError, DocumentTooLargeError
from app.ai.parsers.registry import ParserRegistry
from app.storage.service import StorageService
from app.storage.exceptions import FileNotFoundInStorageError
from models.db.document import Document
from models.enums import ParsingStatus
from core.exceptions import NotFoundError, InvalidStateError

# Re-register defaults for tests
from app.ai.parsers.pdf_parser import PDFParser
ParserRegistry.clear()
ParserRegistry.register(PDFParser())

HELLO_WORLD_PDF_B64 = (
    b"JVBERi0xLjcKCjEgMCBvYmogICUgZW50cnkgcG9pbnQKPDwKICAvVHlwZSAvQ2F0YWxvZwog"
    b"IC9QYWdlcyAyIDAgUgo+PgplbmRvYmoKCjIgMCBvYmogPDwKICAvVHlwZSAvUGFnZXMKICAv"
    b"TWVkaWFCb3ggWyAwIDAgMjAwIDIwMCBdCiAgL0NvdW50IDEKICAvS2lkcyBbIDMgMCBSIF0K"
    b"Pj4KZW5kb2JqCgozIDAgb2JqCjw8CiAgL1R5cGUgL1BhZ2UKICAvUGFyZW50IDIgMCBSCiAg"
    b"L1Jlc291cmNlcyA8PAogICAgL0ZvbnQgPDwKICAgICAgL0YxIDQgMCBSCgkgICAgPj4KICA+"
    b"PgogIC9Db250ZW50cyA1IDAgUgo+PgplbmRvYmoKCjQgMCBvYmoKPDwKICAvVHlwZSAvRm9u"
    b"dAogIC9TdWJ0eXBlIC9UeXBlMQogIC9CYXNlRm9udCAvVGltZXMtUm9tYW4KPj4KZW5kb2Jq"
    b"Cgo1IDAgb2JqICAlIHBhZ2UgY29udGVudAo8PAogIC9MZW5ndGggNDQKPj4Kc3RyZWFtCkJU"
    b"CjcwIDUwIFRECi9GMSAxMiBUZgooSGVsbG8gV29ybGQpIFRqCkVUCmVuZHN0cmVhbQplbmRv"
    b"YmoKCnhyZWYKMCA2CjAwMDAwMDAwMDAgNjU1MzUgZiAKMDAwMDAwMDEwIDEwMDAwIG4gCjAw"
    b"MDAwMDAwNjAgMTAwMDAgbiAKMDAwMDAwMDE1NyAxMDAwMCBuIAowMDAwMDAwMjcyIDEwMDAw"
    b"IG4gCjAwMDAwMDAzNTkgMTAwMDAgbiAKdHJhaWxlcgo8PAogIC9TaXplIDYKICAvUm9vdCAx"
    b"IDAgUgo+PgpzdGFydHhyZWYKNDU0CiUlRU9GCg=="
)

@pytest.fixture
def temp_pdf():
    fd, path = tempfile.mkstemp(suffix=".pdf")
    with os.fdopen(fd, 'wb') as f:
        f.write(base64.b64decode(HELLO_WORLD_PDF_B64))
    yield path
    os.remove(path)

@pytest.fixture
def mock_storage(temp_pdf):
    storage = MagicMock(spec=StorageService)
    # mock get_read_stream to return an open file
    f = open(temp_pdf, 'rb')
    storage.get_read_stream.return_value = f
    yield storage
    f.close()

@pytest.mark.asyncio
async def test_parse_success(test_db, mock_storage):
    user_id = uuid4()
    doc = Document(
        original_filename="test.pdf",
        mime_type="application/pdf",
        extension=".pdf",
        file_size_bytes=1000,
        storage_key=f"test/{uuid4()}.pdf",
        checksum="abcd",
        owner_id=user_id,
        parsing_status=ParsingStatus.PENDING
    )
    test_db.add(doc)
    test_db.commit()

    service = DocumentParserService(db=test_db, storage_service=mock_storage)
    result = await service.parse_document(str(doc.id), str(user_id))

    assert result["status"] == "parsed"
    assert result["pages"] == 1
    assert result["parser"] == "pypdf"

    # Verify DB update
    test_db.refresh(doc)
    assert doc.parsing_status == ParsingStatus.PARSED
    assert "Hello World" in doc.parsed_text
    assert doc.page_count == 1
    assert doc.parse_duration_ms is not None

@pytest.mark.asyncio
async def test_parse_wrong_owner_raises(test_db, mock_storage):
    user_id = uuid4()
    doc = Document(
        original_filename="test.pdf",
        mime_type="application/pdf",
        extension=".pdf",
        file_size_bytes=1000,
        storage_key=f"test/{uuid4()}.pdf",
        checksum="abcd",
        owner_id=user_id,
        parsing_status=ParsingStatus.PENDING
    )
    test_db.add(doc)
    test_db.commit()

    service = DocumentParserService(db=test_db, storage_service=mock_storage)
    with pytest.raises(NotFoundError):
        await service.parse_document(str(doc.id), str(uuid4()))

@pytest.mark.asyncio
async def test_parse_invalid_state(test_db, mock_storage):
    user_id = uuid4()
    doc = Document(
        original_filename="test.pdf",
        mime_type="application/pdf",
        extension=".pdf",
        file_size_bytes=1000,
        storage_key=f"test/{uuid4()}.pdf",
        checksum="abcd",
        owner_id=user_id,
        parsing_status=ParsingStatus.PARSING
    )
    test_db.add(doc)
    test_db.commit()

    service = DocumentParserService(db=test_db, storage_service=mock_storage)
    with pytest.raises(InvalidStateError):
        await service.parse_document(str(doc.id), str(user_id))

@pytest.mark.asyncio
async def test_parse_file_not_found(test_db):
    user_id = uuid4()
    doc = Document(
        original_filename="test.pdf",
        mime_type="application/pdf",
        extension=".pdf",
        file_size_bytes=1000,
        storage_key=f"test/{uuid4()}.pdf",
        checksum="abcd",
        owner_id=user_id,
        parsing_status=ParsingStatus.PENDING
    )
    test_db.add(doc)
    test_db.commit()

    storage = MagicMock(spec=StorageService)
    storage.get_read_stream.side_effect = FileNotFoundInStorageError()

    service = DocumentParserService(db=test_db, storage_service=storage)
    with pytest.raises(ParserError):
        await service.parse_document(str(doc.id), str(user_id))

    test_db.refresh(doc)
    assert doc.parsing_status == ParsingStatus.FAILED
    assert "File not found" in doc.parsing_error
