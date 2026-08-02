from typing import Dict, Any, Tuple
from app.ai.agents.performance.prompts.versions import PROMPT_VERSIONS

class PromptRegistry:
    """Registry to fetch specific versions of prompts."""
    
    @classmethod
    def get_prompt_version(cls, version: str) -> Tuple[str, str]:
        """Returns (system_prompt, developer_prompt) for the requested version."""
        if version not in PROMPT_VERSIONS:
            raise ValueError(f"Prompt version {version} not found in registry.")
            
        mapping = PROMPT_VERSIONS[version]
        return mapping["system"], mapping["developer"]
