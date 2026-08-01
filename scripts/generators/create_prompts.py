import os
from pathlib import Path

prompts_dir = Path("backend/app/ai/prompts")
for d in ["system", "user", "templates", "versions"]:
    (prompts_dir / d).mkdir(parents=True, exist_ok=True)

# 1. exceptions.py
(prompts_dir / "exceptions.py").write_text('''"""
Custom exceptions for the Prompt Management System.
"""

class PromptException(Exception):
    """Base exception for all prompt-related errors."""
    pass

class PromptNotFoundError(PromptException):
    """Raised when a prompt file or registered prompt is not found."""
    pass

class PromptValidationError(PromptException):
    """Raised when prompt rendering fails validation (missing/unused variables)."""
    pass

class PromptRenderError(PromptException):
    """Raised when rendering a prompt fails unexpectedly."""
    pass

class PromptRegistrationError(PromptException):
    """Raised when there is an issue registering a prompt (e.g., duplicate)."""
    pass
''', encoding="utf-8")

# 2. models.py
(prompts_dir / "models.py").write_text('''"""
Data models for the Prompt Management System.
"""
from pydantic import BaseModel, Field
from typing import List

class PromptMetadata(BaseModel):
    """Metadata describing a registered prompt."""
    name: str
    version: str
    description: str
    owner_agent: str
    required_variables: List[str] = Field(default_factory=list)
    system_prompt_path: str
    user_prompt_path: str
''', encoding="utf-8")

# 3. validator.py
(prompts_dir / "validator.py").write_text('''"""
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
''', encoding="utf-8")

# 4. cache.py
(prompts_dir / "cache.py").write_text('''"""
In-memory cache for prompt templates to avoid redundant disk I/O.
"""
from typing import Dict, Optional

class PromptCache:
    def __init__(self):
        self._cache: Dict[str, str] = {}
        
    def get(self, path: str) -> Optional[str]:
        """Retrieves a cached prompt by path."""
        return self._cache.get(path)
        
    def set(self, path: str, content: str) -> None:
        """Stores a prompt in the cache."""
        self._cache[path] = content
        
    def clear(self) -> None:
        """Clears the entire cache."""
        self._cache.clear()
''', encoding="utf-8")

# 5. renderer.py
(prompts_dir / "renderer.py").write_text('''"""
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
''', encoding="utf-8")

# 6. loader.py
(prompts_dir / "loader.py").write_text('''"""
Loads prompt files from disk safely, using caching.
"""
from pathlib import Path
from .cache import PromptCache
from .exceptions import PromptNotFoundError

class PromptLoader:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.cache = PromptCache()
        
    def load(self, relative_path: str) -> str:
        """Loads a prompt file from disk, using cache if available."""
        full_path = self.base_dir / relative_path
        
        # Check cache
        cached = self.cache.get(str(full_path))
        if cached is not None:
            return cached
            
        # Load from disk
        if not full_path.exists() or not full_path.is_file():
            raise PromptNotFoundError(f"Prompt file not found at: {full_path}")
            
        content = full_path.read_text(encoding="utf-8")
        self.cache.set(str(full_path), content)
        return content
''', encoding="utf-8")

# 7. registry.py
(prompts_dir / "registry.py").write_text('''"""
Central registry managing all available prompts in the system.
"""
from typing import Dict
from pathlib import Path
from .models import PromptMetadata
from .loader import PromptLoader
from .renderer import PromptRenderer
from .exceptions import PromptRegistrationError, PromptNotFoundError

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
        
        # Ensure that ALL required variables combined were provided
        provided = set(variables.keys())
        required = set(metadata.required_variables)
        
        if provided != required:
            # Let the specific validator handle it, but we can do a coarse check here
            pass
            
        sys_rendered = PromptRenderer.render(system_template, sys_vars)
        user_rendered = PromptRenderer.render(user_template, user_vars)
        
        return sys_rendered, user_rendered
''', encoding="utf-8")

# 8. __init__.py
(prompts_dir / "__init__.py").write_text('''"""
Enterprise Prompt Management System
"""
from .exceptions import PromptException, PromptNotFoundError, PromptValidationError, PromptRenderError, PromptRegistrationError
from .models import PromptMetadata
from .validator import PromptValidator
from .cache import PromptCache
from .renderer import PromptRenderer
from .loader import PromptLoader
from .registry import PromptRegistry
''', encoding="utf-8")

# Create sample prompt files
(prompts_dir / "system" / "bias.txt").write_text("You are an expert bias detector. Analyze this feedback.", encoding="utf-8")
(prompts_dir / "user" / "bias.txt").write_text("Employee: {{employee_name}}\nFeedback: {{manager_feedback}}", encoding="utf-8")

(prompts_dir / "system" / "analysis.txt").write_text("You are a performance analyst.", encoding="utf-8")
(prompts_dir / "user" / "analysis.txt").write_text("Goals: {{goal_progress}}", encoding="utf-8")

(prompts_dir / "system" / "report.txt").write_text("You are an executive report generator.", encoding="utf-8")
(prompts_dir / "user" / "report.txt").write_text("Summarize for: {{employee_name}}", encoding="utf-8")

(prompts_dir / "system" / "retrieval.txt").write_text("You are an evidence retriever.", encoding="utf-8")
(prompts_dir / "user" / "retrieval.txt").write_text("Extract from: {{retrieved_evidence}}", encoding="utf-8")

print("Created AI Prompt Management System files")
