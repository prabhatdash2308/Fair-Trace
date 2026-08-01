"""
Telemetry tracking for Embedding Service.
"""
import logging

logger = logging.getLogger(__name__)

class Telemetry:
    def __init__(self):
        self.total_requests = 0
        self.total_chunks = 0
        self.total_cost = 0.0
        
    def record_embedding(self, correlation_id: str, model: str, latency_ms: int, chunks: int, cost: float) -> None:
        self.total_requests += 1
        self.total_chunks += chunks
        self.total_cost += cost
        logger.info(f"[EmbeddingTelemetry {correlation_id}] Model: {model} | Latency: {latency_ms}ms | Chunks: {chunks} | Cost: ")
