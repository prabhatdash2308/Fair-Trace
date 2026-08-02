from typing import Dict, Type
from app.export.exceptions import ExportError

class ExportProviderRegistry:
    _providers: Dict[str, Type] = {}
    
    @classmethod
    def register(cls, name: str):
        def decorator(provider_class: Type):
            cls._providers[name] = provider_class
            return provider_class
        return decorator
        
    @classmethod
    def get(cls, name: str):
        provider = cls._providers.get(name)
        if not provider:
            raise ExportError(f"Provider {name} not found")
        return provider()
