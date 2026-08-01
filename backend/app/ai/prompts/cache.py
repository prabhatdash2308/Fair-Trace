"""
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
