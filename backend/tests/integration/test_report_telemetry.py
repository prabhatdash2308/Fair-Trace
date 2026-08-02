import pytest
from app.ai.agents.report.utils import generate_prompt_hash, estimate_tokens

def test_report_generate_prompt_hash():
    sys = "Sys"
    dev = "Dev"
    hash1 = generate_prompt_hash(sys, dev)
    hash2 = generate_prompt_hash(sys, dev)
    assert hash1 == hash2

def test_report_estimate_tokens():
    tokens = estimate_tokens("Hello world")
    assert tokens > 0
