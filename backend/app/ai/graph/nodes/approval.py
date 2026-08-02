import structlog
from typing import Dict, Any
from langgraph.errors import NodeInterrupt

from app.ai.graph.nodes.base import BaseNode
from app.ai.graph.models import NodeResult
from app.ai.graph.registry import NodeRegistry

logger = structlog.get_logger(__name__)

@NodeRegistry.register("approval_node")
class ApprovalNode(BaseNode):
    """
    Human-in-the-Loop Approval Node.
    Uses NodeInterrupt to pause execution and wait for Command(resume=decision).
    """
    
    def validate(self, state: Dict[str, Any]) -> None:
        if not state.get("final_report"):
            raise ValueError("final_report is required before Human Approval")
            
    def before(self, state: Dict[str, Any]) -> None:
        pass
        
    async def execute(self, state: Dict[str, Any]) -> NodeResult:
        # Check if we just got a resume decision
        approval_state = state.get("approval")
        
        # If we have a decision in the state and it's resolved, we are resuming
        if approval_state and approval_state.get("status") == "resolved":
            decision = approval_state.get("decision", "unknown")
            logger.info("resuming_from_human_approval", decision=decision)
            return NodeResult(
                status="success",
                data={"decision": decision}
            )
            
        # Otherwise, pause for human approval
        logger.info("interrupting_for_human_approval", execution_id=state.get("execution_id"))
        raise NodeInterrupt("waiting for approval")
        
        return NodeResult(
            status="success",
            data={"decision": decision}
        )
        
    def after(self, state: Dict[str, Any], result: NodeResult) -> None:
        # Populate the state.approval dictionary based on the human decision
        if "approval" not in state or state["approval"] is None:
            state["approval"] = {}
            
        decision = result.data.get("decision", "unknown")
        state["approval"]["decision"] = decision
        state["approval"]["status"] = "resolved"
