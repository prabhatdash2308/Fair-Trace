from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseProvider(ABC):
    @abstractmethod
    def render(self, report: Dict[str, Any], metadata: Dict[str, Any]) -> bytes:
        pass
