"""
Observability and metrics tracking.
"""
import logging
from typing import Optional
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class Telemetry:
    def __init__(self):
        self.total_requests = 0
        self.total_errors = 0
        self.total_cost = 0.0
        
    def record_request(self, correlation_id: str, model: str, latency_ms: int, tokens: int, cost: float) -> None:
        self.total_requests += 1
        self.total_cost += cost
        logger.info(f"[Telemetry {correlation_id}] Model: {model} | Latency: {latency_ms}ms | Tokens: {tokens} | Cost: ")
        
    def record_error(self, correlation_id: str, error: Exception) -> None:
        self.total_errors += 1
        logger.error(f"[Telemetry {correlation_id}] Error: {str(error)}")
