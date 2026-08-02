import pytest
from app.ai.agents.bias.utils import generate_prompt_hash, estimate_tokens

def test_bias_generate_prompt_hash():
    sys = "Sys"
    dev = "Dev"
    hash1 = generate_prompt_hash(sys, dev)
    hash2 = generate_prompt_hash(sys, dev)
    assert hash1 == hash2
    
    hash3 = generate_prompt_hash(sys, dev + " ")
    assert hash1 != hash3

def test_bias_estimate_tokens():
    tokens = estimate_tokens("Hello world")
    assert tokens > 0
