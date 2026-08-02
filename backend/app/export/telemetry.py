import structlog
from typing import Dict, Any

logger = structlog.get_logger(__name__)

class ExportTelemetry:
    @staticmethod
    def log_event(event_name: str, **kwargs):
        logger.info(event_name, **kwargs)
