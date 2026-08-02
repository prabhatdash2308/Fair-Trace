from typing import Dict, Any, List
import structlog
from abc import ABC, abstractmethod

class NotificationProvider(ABC):
    @abstractmethod
    def send(self, recipient: str, subject: str, message: str, metadata: Dict[str, Any] = None) -> bool:
        pass
        
    @abstractmethod
    def send_bulk(self, recipients: List[str], subject: str, message: str, metadata: Dict[str, Any] = None) -> Dict[str, bool]:
        pass
        
    @abstractmethod
    def health(self) -> Dict[str, Any]:
        pass
        
    @abstractmethod
    def version(self) -> str:
        pass

class LogProvider(NotificationProvider):
    def __init__(self):
        self.logger = structlog.get_logger(__name__)
        
    def send(self, recipient: str, subject: str, message: str, metadata: Dict[str, Any] = None) -> bool:
        self.logger.info("notification_sent", provider="LogProvider", recipient=recipient, subject=subject, metadata=metadata)
        return True
        
    def send_bulk(self, recipients: List[str], subject: str, message: str, metadata: Dict[str, Any] = None) -> Dict[str, bool]:
        results = {}
        for r in recipients:
            results[r] = self.send(r, subject, message, metadata)
        return results
        
    def health(self) -> Dict[str, Any]:
        return {"status": "healthy"}
        
    def version(self) -> str:
        return "1.0"
        
class NotificationService:
    _provider = LogProvider()
    
    @classmethod
    def set_provider(cls, provider: NotificationProvider):
        cls._provider = provider
        
    @classmethod
    def notify(cls, recipient: str, subject: str, message: str, metadata: Dict[str, Any] = None) -> bool:
        return cls._provider.send(recipient, subject, message, metadata)
