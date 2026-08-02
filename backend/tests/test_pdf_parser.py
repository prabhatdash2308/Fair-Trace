import pytest
import os
import tempfile
import base64
from pypdf import PdfWriter
from app.ai.parsers.pdf_parser import PDFParser
from app.ai.parsers.exceptions import NoTextFoundError, EncryptedDocumentError

@pytest.fixture
def parser():
    return PDFParser()

def create_temp_file(content: bytes, suffix=".pdf") -> str:
    fd, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(fd, 'wb') as f:
        f.write(content)
    return path

# A minimal valid PDF containing the text "Hello World"
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

def test_parse_valid_pdf(parser):
    path = create_temp_file(base64.b64decode(HELLO_WORLD_PDF_B64))
    try:
        doc = parser.parse(path)
        assert "Hello World" in doc.text
        assert doc.page_count == 1
    finally:
        os.remove(path)

def test_empty_pdf_raises_no_text(parser):
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    
    fd, path = tempfile.mkstemp(suffix=".pdf")
    os.close(fd)
    writer.write(path)
    
    try:
        with pytest.raises(NoTextFoundError):
            parser.parse(path)
    finally:
        os.remove(path)

def test_encrypted_pdf_raises(parser):
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    writer.encrypt("secret")
    
    fd, path = tempfile.mkstemp(suffix=".pdf")
    os.close(fd)
    writer.write(path)
    
    try:
        with pytest.raises(EncryptedDocumentError):
            parser.parse(path)
    finally:
        os.remove(path)
