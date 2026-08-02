import pytest
from app.export.utils import generate_checksum, generate_signature

def test_generate_checksum():
    assert generate_checksum("test") == "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"

def test_generate_signature():
    sig = generate_signature(
        report_json='{"test": 1}',
        workflow_id="wf-1",
        approval_timestamp="2024-01-01T00:00:00Z",
        reviewer_id="user-1",
        version="1.0"
    )
    assert len(sig) == 64  # SHA256 length
