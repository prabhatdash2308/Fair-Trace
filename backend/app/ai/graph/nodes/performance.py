import structlog
from typing import Dict, Any

from app.ai.graph.nodes.base import BaseNode
from app.ai.graph.models import NodeResult
from app.ai.graph.registry import NodeRegistry
from app.ai.agents.performance.service import PerformanceAnalysisService

logger = structlog.get_logger(__name__)

@NodeRegistry.register("performance_node")
class PerformanceNode(BaseNode):
    
    def validate(self, state: Dict[str, Any]) -> None:
        if not state.get("context_bundle"):
            raise ValueError("context_bundle is required for Performance Analysis")
            
    def before(self, state: Dict[str, Any]) -> None:
        pass
        
    async def execute(self, state: Dict[str, Any]) -> NodeResult:
        logger.info("Executing Enterprise Performance Analysis Agent")
        
        # Invoke the robust agent service
        analysis = await PerformanceAnalysisService.analyze_context(state)
        
        return NodeResult(
            status="success",
            data=analysis
        )
        
    def after(self, state: Dict[str, Any], result: NodeResult) -> None:
        state["performance_analysis"] = result.data
