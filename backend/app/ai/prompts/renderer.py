"""
Safely renders prompt templates with provided variables.
"""
from typing import Dict, Any
from .validator import PromptValidator
from .exceptions import PromptRenderError

class PromptRenderer:
    @staticmethod
    def render(template: str, variables: Dict[str, Any]) -> str:
        """
        Renders the template by replacing {{key}} with value.
        """
        PromptValidator.validate_rendering(template, variables)
        
        rendered = template
        try:
            for key, value in variables.items():
                rendered = rendered.replace(f"{{{{{key}}}}}", str(value))
            return rendered
        except Exception as e:
            raise PromptRenderError(f"Failed to render prompt: {str(e)}") from e
