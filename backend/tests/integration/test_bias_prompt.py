import pytest
from app.ai.agents.bias.prompts.registry import PromptRegistry

def test_bias_prompt_registry_valid_version():
    sys, dev = PromptRegistry.get_prompt_version("1.0")
    assert "Enterprise AI HR Auditor" in sys
    assert "overall_bias_score" in dev

def test_bias_prompt_registry_invalid_version():
    with pytest.raises(ValueError, match="not found in registry"):
        PromptRegistry.get_prompt_version("99.9")
