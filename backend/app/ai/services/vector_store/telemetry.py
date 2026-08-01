"""
Telemetry tracking for Vector Store Service.
"""
import logging

logger = logging.getLogger(__name__)

class Telemetry:
    def __init__(self):
        self.search_count = 0
        self.upsert_count = 0
        self.delete_count = 0
        self.health_checks = 0
        
    def record_search(self, correlation_id: str, latency_ms: int, results_count: int) -> None:
        self.search_count += 1
        logger.info(f"[VectorStore {correlation_id}] Search | Latency: {latency_ms}ms | Matches: {results_count}")
        
    def record_upsert(self, correlation_id: str, latency_ms: int, vector_count: int) -> None:
        self.upsert_count += 1
        logger.info(f"[VectorStore {correlation_id}] Upsert | Latency: {latency_ms}ms | Count: {vector_count}")
        
    def record_delete(self, correlation_id: str, latency_ms: int, delete_count: int) -> None:
        self.delete_count += 1
        logger.info(f"[VectorStore {correlation_id}] Delete | Latency: {latency_ms}ms | Count: {delete_count}")
        
    def record_health_check(self, latency_ms: int, is_healthy: bool) -> None:
        self.health_checks += 1
        status = "Healthy" if is_healthy else "Unhealthy"
        logger.info(f"[VectorStore] HealthCheck | Latency: {latency_ms}ms | Status: {status}")
