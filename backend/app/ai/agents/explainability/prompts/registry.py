from typing import Tuple
from app.ai.agents.explainability.prompts.versions import PROMPT_VERSIONS

class PromptRegistry:
    @classmethod
    def get_prompt_version(cls, version: str) -> Tuple[str, str]:
        if version not in PROMPT_VERSIONS:
            raise ValueError(f"Prompt version {version} not found in registry.")
            
        mapping = PROMPT_VERSIONS[version]
        return mapping["system"], mapping["developer"]
