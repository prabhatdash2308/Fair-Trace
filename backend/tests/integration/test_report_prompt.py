import pytest
from app.ai.agents.report.prompts.registry import PromptRegistry

def test_report_prompt_registry_valid_version():
    sys, dev = PromptRegistry.get_prompt_version("1.0")
    assert "Enterprise Report Generation Engine" in sys
    assert "DO NOT HALLUCINATE" in sys

def test_report_prompt_registry_invalid_version():
    with pytest.raises(ValueError, match="not found in registry"):
        PromptRegistry.get_prompt_version("99.9")
