from typing import Dict, Any

class InterruptManager:
    """
    Handles graph suspension conditions.
    """
    
    @staticmethod
    def should_interrupt(state: Dict[str, Any], current_node: str) -> bool:
        """Determines if the graph should halt execution natively."""
        # For Human Approval node
        if current_node == "approval_node" and not state.get("approval", {}).get("is_approved"):
            return True
        return False
