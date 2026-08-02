from app.ai.graph.nodes.base import BaseNode
from app.ai.graph.state import ReviewState
from app.ai.graph.models import NodeResult
from app.ai.graph.registry import NodeRegistry

@NodeRegistry.register(name="preprocess_node", description="Preprocesses text.", dependencies=["load_context_node"])
class PreprocessNode(BaseNode):
    async def execute(self, state: ReviewState) -> NodeResult:
        # Stub logic
        return NodeResult(
            state={"metadata": {"current_node": "preprocess"}},
            status="completed"
        )
