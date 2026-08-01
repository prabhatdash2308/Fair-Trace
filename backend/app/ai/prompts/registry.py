"""
Central registry managing all available prompts in the system.
"""
from typing import Dict
from pathlib import Path
from .models import PromptMetadata
from .loader import PromptLoader
from .renderer import PromptRenderer
from .exceptions import PromptRegistrationError, PromptNotFoundError, PromptValidationError

class PromptRegistry:
    def __init__(self, loader: PromptLoader):
        self.loader = loader
        self._prompts: Dict[str, PromptMetadata] = {}
        
    def register(self, metadata: PromptMetadata) -> None:
        """Registers a new prompt metadata entry."""
        if metadata.name in self._prompts:
            raise PromptRegistrationError(f"Prompt '{metadata.name}' is already registered.")
            
        # Validate files exist by dry-loading them
        try:
            self.loader.load(metadata.system_prompt_path)
            self.loader.load(metadata.user_prompt_path)
        except PromptNotFoundError as e:
            raise PromptRegistrationError(f"Cannot register '{metadata.name}': {str(e)}")
            
        self._prompts[metadata.name] = metadata
        
    def get_prompt(self, name: str) -> PromptMetadata:
        """Retrieves metadata for a registered prompt."""
        if name not in self._prompts:
            raise PromptNotFoundError(f"Prompt '{name}' is not registered.")
        return self._prompts[name]
        
    def render_prompt(self, name: str, variables: Dict[str, str]) -> tuple[str, str]:
        """
        Loads and renders both system and user prompts.
        Returns (rendered_system_prompt, rendered_user_prompt).
        """
        metadata = self.get_prompt(name)
        
        system_template = self.loader.load(metadata.system_prompt_path)
        user_template = self.loader.load(metadata.user_prompt_path)
        
        # Split variables if needed, or pass all to both and allow subset? 
        # For strict validation, we might need to filter variables per template.
        # But for this implementation, we will pass variables globally.
        # However our strict validator checks for unused vars.
        # So we extract vars for each template.
        from .validator import PromptValidator
        sys_vars = {k: variables[k] for k in PromptValidator.extract_placeholders(system_template) if k in variables}
        user_vars = {k: variables[k] for k in PromptValidator.extract_placeholders(user_template) if k in variables}
        
        provided = set(variables.keys())
        required = set(metadata.required_variables)
        
        missing = required - provided
        if missing:
            raise PromptValidationError(f"Missing required variables for prompt '{name}': {missing}")
            
        unused = provided - required
        if unused:
            raise PromptValidationError(f"Unused variables provided for prompt '{name}': {unused}")
            
        sys_rendered = PromptRenderer.render(system_template, sys_vars)
        user_rendered = PromptRenderer.render(user_template, user_vars)
        
        return sys_rendered, user_rendered
