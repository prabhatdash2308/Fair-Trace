import structlog
from typing import Dict, Any

from app.ai.graph.nodes.base import BaseNode
from app.ai.graph.models import NodeResult
from app.ai.graph.registry import NodeRegistry
from app.ai.agents.bias.service import BiasAnalysisService

logger = structlog.get_logger(__name__)

@NodeRegistry.register("bias_node")
class BiasNode(BaseNode):
    
    def validate(self, state: Dict[str, Any]) -> None:
        if not state.get("performance_analysis"):
            raise ValueError("performance_analysis is required for Bias Detection")
        if not state.get("context_bundle"):
            raise ValueError("context_bundle is required for Bias Detection")
            
    def before(self, state: Dict[str, Any]) -> None:
        pass
        
    async def execute(self, state: Dict[str, Any]) -> NodeResult:
        logger.info("Executing Enterprise Bias Detection Agent")
        
        # Invoke the robust agent service
        bias_full_data = await BiasAnalysisService.analyze_context(state)
        
        return NodeResult(
            status="success",
            data=bias_full_data
        )
        
    def after(self, state: Dict[str, Any], result: NodeResult) -> None:
        state["bias_analysis"] = result.data.get("analysis")
        state["bias_metrics"] = {
            "count": len(result.data.get("analysis", {}).get("detected_biases", []))
        }
        state["bias_cost"] = result.data.get("cost_metrics")
        state["bias_metadata"] = result.data.get("metadata")
