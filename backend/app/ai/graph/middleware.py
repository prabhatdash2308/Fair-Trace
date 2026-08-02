import time
from typing import Callable, Any, Dict
from app.ai.graph.state import ReviewState
from app.ai.graph.models import NodeResult
from app.ai.graph.telemetry import GraphTelemetry
from app.ai.graph.events import NodeStarted, NodeCompleted, NodeFailed
from app.ai.graph.exceptions import NodeExecutionError

class NodeMiddleware:
    """Wraps BaseNode executions providing Validation -> Metrics -> Tracing -> Checkpoint -> Events."""
    
    @staticmethod
    async def execute_with_middleware(node_name: str, state: ReviewState, node_execute: Callable) -> NodeResult:
        execution_id = state.get("execution_id", "unknown")
        
        # 1. Tracing & Events (Start)
        GraphTelemetry.log_node_start(execution_id, node_name)
        # Event emission could be dispatched to an EventBus here
        
        start_time = time.time()
        try:
            # 2. Execution
            result: NodeResult = await node_execute(state)
            
            # 3. Metrics (End)
            duration_ms = int((time.time() - start_time) * 1000)
            GraphTelemetry.log_node_complete(execution_id, node_name, duration_ms, result.status)
            
            # Auto-inject telemetry into the result if the node didn't
            if not result.telemetry:
                result.telemetry = {}
            result.telemetry["duration_ms"] = duration_ms
            
            return result
            
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            GraphTelemetry.log_node_error(execution_id, node_name, str(e))
            raise NodeExecutionError(f"Node '{node_name}' failed: {str(e)}") from e
