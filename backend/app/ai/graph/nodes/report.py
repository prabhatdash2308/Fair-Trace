import structlog
from typing import Dict, Any

from app.ai.graph.nodes.base import BaseNode
from app.ai.graph.models import NodeResult
from app.ai.graph.registry import NodeRegistry
from app.ai.agents.report.service import ReportGenerationService

logger = structlog.get_logger(__name__)

@NodeRegistry.register("report_node")
class ReportNode(BaseNode):
    
    def validate(self, state: Dict[str, Any]) -> None:
        if not state.get("performance_analysis"):
            raise ValueError("performance_analysis is required for Report Generation")
        if not state.get("bias_analysis"):
            raise ValueError("bias_analysis is required for Report Generation")
        if not state.get("explainability_analysis"):
            raise ValueError("explainability_analysis is required for Report Generation")
        if not state.get("context_bundle"):
            raise ValueError("context_bundle is required for Report Generation")
            
    def before(self, state: Dict[str, Any]) -> None:
        pass
        
    async def execute(self, state: Dict[str, Any]) -> NodeResult:
        logger.info("Executing Enterprise Report Generation Agent")
        
        report_full_data = await ReportGenerationService.generate_report(state)
        
        return NodeResult(
            status="success",
            data=report_full_data
        )
        
    def after(self, state: Dict[str, Any], result: NodeResult) -> None:
        state["final_report"] = result.data.get("report")
        state["report_metrics"] = result.data.get("pipeline_metrics")
        state["report_cost"] = result.data.get("cost_metrics")
        state["report_metadata"] = result.data.get("metadata")
