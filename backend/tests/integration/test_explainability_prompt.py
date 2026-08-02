import pytest
from app.ai.agents.explainability.prompts.registry import PromptRegistry

def test_explainability_prompt_registry_valid_version():
    sys, dev = PromptRegistry.get_prompt_version("1.0")
    assert "Enterprise AI Explainability Engine" in sys
    assert "overall_confidence" in dev or "Confidence:" in dev

def test_explainability_prompt_registry_invalid_version():
    with pytest.raises(ValueError, match="not found in registry"):
        PromptRegistry.get_prompt_version("99.9")
