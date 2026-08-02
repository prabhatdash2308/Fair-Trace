import structlog
from typing import Dict, Any

from app.ai.graph.nodes.base import BaseNode
from app.ai.graph.models import NodeResult
from app.ai.graph.registry import NodeRegistry
from app.ai.agents.explainability.service import ExplainabilityAnalysisService

logger = structlog.get_logger(__name__)

@NodeRegistry.register("explainability_node")
class ExplainabilityNode(BaseNode):
    
    def validate(self, state: Dict[str, Any]) -> None:
        if not state.get("performance_analysis"):
            raise ValueError("performance_analysis is required for Explainability")
        if not state.get("bias_analysis"):
            raise ValueError("bias_analysis is required for Explainability")
        if not state.get("context_bundle"):
            raise ValueError("context_bundle is required for Explainability")
            
    def before(self, state: Dict[str, Any]) -> None:
        pass
        
    async def execute(self, state: Dict[str, Any]) -> NodeResult:
        logger.info("Executing Enterprise Explainability Agent")
        
        explainability_full_data = await ExplainabilityAnalysisService.analyze_context(state)
        
        return NodeResult(
            status="success",
            data=explainability_full_data
        )
        
    def after(self, state: Dict[str, Any], result: NodeResult) -> None:
        state["explainability_analysis"] = result.data.get("analysis")
        state["explainability_metrics"] = {
            "reasoning_steps": len(result.data.get("analysis", {}).get("reasoning_trace", []))
        }
        state["explainability_cost"] = result.data.get("cost_metrics")
        state["explainability_metadata"] = result.data.get("metadata")
