from app.ai.graph.nodes.base import BaseNode
from app.ai.graph.state import ReviewState
from app.ai.graph.models import NodeResult
from app.ai.graph.exceptions import NodeExecutionError
from app.ai.graph.registry import NodeRegistry

@NodeRegistry.register(name="load_context_node", description="Loads ContextBundle from DB.")
class LoadContextNode(BaseNode):
    async def validate(self, state: ReviewState):
        if "context_bundle" not in state or not state["context_bundle"]:
            raise NodeExecutionError("context_bundle is required for LoadContextNode")

    async def execute(self, state: ReviewState) -> NodeResult:
        # Stub logic
        return NodeResult(
            state={"metadata": {"current_node": "load_context"}},
            status="completed"
        )
