import pytest
import os
import tempfile
from app.ai.parsers.txt_parser import TXTParser
from app.ai.parsers.exceptions import NoTextFoundError, ParsingFailedError

@pytest.fixture
def parser():
    return TXTParser()

def create_temp_file(content: bytes, suffix=".txt") -> str:
    fd, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(fd, 'wb') as f:
        f.write(content)
    return path

def test_parse_utf8(parser):
    path = create_temp_file("Hello World 你好".encode("utf-8"))
    try:
        doc = parser.parse(path)
        assert "Hello World 你好" in doc.text
        assert doc.metadata["encoding"] == "utf_8"
    finally:
        os.remove(path)

def test_parse_utf16(parser):
    path = create_temp_file("Hello UTF-16 你好".encode("utf-16"))
    try:
        doc = parser.parse(path)
        assert "Hello UTF-16 你好" in doc.text
        assert doc.metadata["encoding"] == "utf_16"
    finally:
        os.remove(path)



def test_empty_txt_raises_no_text(parser):
    path = create_temp_file(b"")
    try:
        with pytest.raises(NoTextFoundError): # empty file returns empty string, raising NoTextFoundError
            parser.parse(path)
    finally:
        os.remove(path)

def test_whitespace_only_raises_no_text(parser):
    path = create_temp_file("   \n \t ".encode("utf-8"))
    try:
        with pytest.raises(NoTextFoundError):
            parser.parse(path)
    finally:
        os.remove(path)
