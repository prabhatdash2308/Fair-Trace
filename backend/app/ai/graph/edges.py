"""
Graph Edges defining conditional routing for the Enterprise Workflow.
"""
from app.ai.state.review_state import ReviewState, PipelineStatus

def default_router(state: ReviewState, next_node: str) -> str:
    if state.metadata.pipeline_status == PipelineStatus.FAILED:
        return "END"
    if state.execution.current_step in state.execution.failed_steps:
        return "retry_node"
    return next_node

def route_after_intake(state: ReviewState) -> str:
    return default_router(state, "embedding")

def route_after_embedding(state: ReviewState) -> str:
    return default_router(state, "evidence_retrieval")

def route_after_retrieval(state: ReviewState) -> str:
    return default_router(state, "bias_detection")

def route_after_bias(state: ReviewState) -> str:
    return default_router(state, "performance_analysis")

def route_after_analysis(state: ReviewState) -> str:
    return default_router(state, "explainability_step")

def route_after_explainability_step(state: ReviewState) -> str:
    return default_router(state, "report_generation")

def route_after_report(state: ReviewState) -> str:
    return default_router(state, "human_approval")

def decision_router(state: ReviewState) -> str:
    if state.metadata.pipeline_status == PipelineStatus.FAILED:
        return "END"
    if state.execution.current_step in state.execution.failed_steps:
        return "retry_node"
        
    status = state.approval.approval_status
    if status == "APPROVED":
        return "finalization"
    elif status == "REVISION_REQUESTED":
        return "report_generation"
    elif status == "REJECTED":
        return "END"
    else:
        # PENDING or unexpected -> halt/end for interrupt. LangGraph interrupt_after pauses it anyway.
        # When resumed, if status is changed to APPROVED, it will route correctly.
        # But wait, interrupt pauses the graph AFTER the human_approval node.
        # When resumed, the state is evaluated by this edge. So this edge MUST route properly.
        # If it's still PENDING when resumed (which shouldn't happen if they mutated state), we end.
        return "END"

def retry_router(state: ReviewState) -> str:
    if state.metadata.pipeline_status == PipelineStatus.FAILED:
        return "END"
    # Resume to the node that failed
    return state.execution.current_step
