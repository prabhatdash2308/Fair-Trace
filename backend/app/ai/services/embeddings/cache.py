"""
Caching for embeddings to save cost and latency.
"""
import hashlib
from typing import Optional, List

class EmbeddingCache:
    def __init__(self):
        self._cache = {}
        
    def _hash(self, text: str, model: str) -> str:
        return hashlib.sha256(f"{model}:{text}".encode('utf-8')).hexdigest()
        
    def get(self, text: str, model: str) -> Optional[List[float]]:
        return self._cache.get(self._hash(text, model))
        
    def set(self, text: str, model: str, vector: List[float]) -> None:
        self._cache[self._hash(text, model)] = vector
