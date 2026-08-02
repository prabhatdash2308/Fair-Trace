from langgraph.graph import StateGraph, START, END
from app.ai.graph.state import ReviewState
from app.ai.graph.registry import NodeRegistry
from app.ai.graph.checkpointer import GraphCheckpointer
from app.ai.graph.middleware import NodeMiddleware
from app.ai.graph.exceptions import GraphExecutionError

# Make sure nodes are imported so the registry populates
import app.ai.graph.nodes.load_context
import app.ai.graph.nodes.preprocess
import app.ai.graph.nodes.performance
import app.ai.graph.nodes.bias
import app.ai.graph.nodes.explainability
import app.ai.graph.nodes.approval
import app.ai.graph.nodes.report

class GraphBuilder:
    """Enterprise Graph Orchestrator mapping sequential deterministic business flow."""
    
    @staticmethod
    def build_graph():
        workflow = StateGraph(ReviewState)
        
        # 1. Instantiate Nodes
        nodes = NodeRegistry.list_nodes()
        node_instances = {}
        
        # To avoid late binding closure issues in loops
        def make_wrapper(node_name, node_instance):
            async def wrapper(state: ReviewState):
                result = await NodeMiddleware.execute_with_middleware(node_name, state, node_instance.run)
                updated_state = state.copy()
                for key, val in result.state.items():
                    # Handle nested dictionary updates deterministically instead of pure overwrite if it's a dict
                    if isinstance(val, dict) and isinstance(updated_state.get(key), dict):
                        updated_state[key] = {**updated_state[key], **val}
                    else:
                        updated_state[key] = val
                return updated_state
            return wrapper
            
        for name, definition in nodes.items():
            instance = definition.node_class()
            node_instances[name] = instance
            workflow.add_node(name, make_wrapper(name, instance))
            
        # 3. Edges
        workflow.add_edge(START, "load_context_node")
        workflow.add_edge("load_context_node", "preprocess_node")
        workflow.add_edge("preprocess_node", "performance_node")
        workflow.add_edge("performance_node", "bias_node")
        workflow.add_edge("bias_node", "explainability_node")
        workflow.add_edge("explainability_node", "report_node")
        workflow.add_edge("report_node", "approval_node")
        workflow.add_edge("approval_node", END)
        
        # 4. Compile
        from app.workflows.checkpoint_service import CheckpointService
        checkpointer = CheckpointService.get_checkpointer()
        compiled = workflow.compile(
            checkpointer=checkpointer
        )
        return compiled
