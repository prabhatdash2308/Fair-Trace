"""
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
