"""
Validates prompts and rendering inputs.
"""
import re
from typing import List, Dict, Any
from .exceptions import PromptValidationError, PromptNotFoundError
from .models import PromptMetadata

class PromptValidator:
    @staticmethod
    def extract_placeholders(template: str) -> List[str]:
        """Extracts all {{variable}} placeholders from a template string."""
        return re.findall(r"\{\{([^}]+)\}\}", template)
        
    @staticmethod
    def validate_rendering(template: str, variables: Dict[str, Any]) -> None:
        """
        Validates that all placeholders in the template are provided in variables,
        and no extra variables are provided (unless desired, here we strictly enforce).
        """
        placeholders = set(PromptValidator.extract_placeholders(template))
        provided = set(variables.keys())
        
        missing = placeholders - provided
        if missing:
            raise PromptValidationError(f"Missing required variables for rendering: {missing}")
            
        unused = provided - placeholders
        # We might just warn about unused, but per instructions we can raise or just let it pass
        # Let's be strict:
        if unused:
            raise PromptValidationError(f"Unused variables provided for rendering: {unused}")

    @staticmethod
    def validate_registration(metadata: PromptMetadata, existing_names: List[str]) -> None:
        """Validates prompt registration data."""
        if metadata.name in existing_names:
            pass # duplicate check handled in registry, but this is a helper
