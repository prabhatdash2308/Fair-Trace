from typing import Dict, Any, Optional
from langgraph.graph.state import CompiledStateGraph
from app.ai.graph.builder import GraphBuilder
from app.ai.graph.exceptions import GraphExecutionError, ResumeError, CancellationError
import datetime

class GraphExecutor:
    """Executes the compiled LangGraph logic natively and deterministically."""
    
    _graph: Optional[CompiledStateGraph] = None

    @classmethod
    def get_graph(cls) -> CompiledStateGraph:
        if cls._graph is None:
            cls._graph = GraphBuilder.build_graph()
        return cls._graph

    @classmethod
    async def run(cls, execution_id: str, state: Dict[str, Any]) -> Dict[str, Any]:
        """Initiate the graph execution."""
        graph = cls.get_graph()
        config = {"configurable": {"thread_id": execution_id}}
        
        # Inject standard metadata
        if "metadata" not in state:
            state["metadata"] = {}
        state["metadata"].update({
            "execution_id": execution_id,
            "started_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "status": "running"
        })
        
        try:
            result = await graph.ainvoke(state, config)
            return result
        except Exception as e:
            raise GraphExecutionError(f"Graph run failed: {str(e)}") from e

    @classmethod
    async def resume(cls, execution_id: str, state_update: Dict[str, Any]) -> Dict[str, Any]:
        """Resume a suspended graph (e.g., after Human Approval)."""
        graph = cls.get_graph()
        config = {"configurable": {"thread_id": execution_id}}
        
        current_state = await graph.aget_state(config)
        if not current_state:
            raise ResumeError(f"Cannot resume. No active state found for execution_id: {execution_id}")
            
        if not current_state.next:
            raise ResumeError(f"Cannot resume. Graph {execution_id} is not paused (no next steps).")

        try:
            # We use `update_state` to inject the user's approval input, then `ainvoke` with None
            await graph.aupdate_state(config, state_update)
            result = await graph.ainvoke(None, config)
            return result
        except Exception as e:
            raise GraphExecutionError(f"Graph resume failed: {str(e)}") from e

    @classmethod
    async def get_status(cls, execution_id: str) -> Dict[str, Any]:
        """Fetch the current state and node of the running graph."""
        graph = cls.get_graph()
        config = {"configurable": {"thread_id": execution_id}}
        current_state = await graph.aget_state(config)
        
        if not current_state:
            return {"status": "not_found", "execution_id": execution_id}
            
        state_values = current_state.values
        metadata = state_values.get("metadata", {})
        
        return {
            "execution_id": execution_id,
            "status": "paused" if current_state.next else metadata.get("status", "unknown"),
            "current_node": metadata.get("current_node"),
            "next_nodes": current_state.next
        }
