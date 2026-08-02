import structlog
from typing import Dict, Any

logger = structlog.get_logger(__name__)

class GraphTelemetry:
    """Enterprise structural logging for LangGraph executions."""
    
    @staticmethod
    def log_node_start(execution_id: str, node_name: str):
        logger.info(
            "graph_node_started",
            execution_id=execution_id,
            node_name=node_name
        )

    @staticmethod
    def log_node_complete(execution_id: str, node_name: str, duration_ms: int, status: str = "completed"):
        logger.info(
            "graph_node_completed",
            execution_id=execution_id,
            node_name=node_name,
            duration_ms=duration_ms,
            status=status
        )

    @staticmethod
    def log_node_error(execution_id: str, node_name: str, error: str):
        logger.error(
            "graph_node_failed",
            execution_id=execution_id,
            node_name=node_name,
            error=error
        )
        
    @staticmethod
    def log_graph_execution(execution_id: str, duration_ms: int, status: str, metadata: Dict[str, Any]):
        logger.info(
            "graph_execution_completed",
            execution_id=execution_id,
            duration_ms=duration_ms,
            status=status,
            checkpoint_count=metadata.get("checkpoint_count", 0),
            interrupt_count=metadata.get("interrupt_count", 0),
            retry_count=metadata.get("retry_count", 0)
        )
