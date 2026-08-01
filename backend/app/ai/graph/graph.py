"""
ReviewGuard AI — LangGraph Pipeline Orchestration Graph
Defines the DAG with all conditional edges for P1, P3, P4 enforcement.

Node execution order:
  intake_agent
  → embedding_agent
  → [evidence_retrieval_agent || bias_detection_agent]  (parallel)
  → performance_analysis_agent
  → report_generation_agent
  → explainability_agent
  → human_approval_agent  (interrupt)
  → [finalization_agent || REVISION → report_generation_agent || REJECT → END]
"""

from langgraph.graph import StateGraph, END

from app.ai.state.review_state import ReviewGuardState
from app.ai.agents.intake_agent import intake_agent_node
from app.ai.agents.embedding_agent import embedding_agent_node
from app.ai.agents.evidence_retrieval_agent import evidence_retrieval_node
from app.ai.agents.bias_detection_agent import bias_detection_node
from app.ai.agents.performance_analysis_agent import performance_analysis_node
from app.ai.agents.report_generation_agent import report_generation_node
from app.ai.agents.explainability_agent import explainability_node
from app.ai.agents.human_approval_agent import human_approval_node
from app.ai.agents.finalization_agent import finalization_node


# ── Routing Functions ──────────────────────────────────────────────────────────

def route_after_intake(state: ReviewGuardState) -> str:
    """P1 gate: if intake failed, end pipeline."""
    if not state.get("intake_complete"):
        return "end"
    return "embedding"


def route_after_embedding(state: ReviewGuardState) -> str:
    """Continue to parallel evidence/bias retrieval."""
    if not state.get("embedding_complete"):
        return "end"
    return "evidence"


def route_after_evidence(state: ReviewGuardState) -> str:
    """P1 gate: evidence_ready must be True."""
    if not state.get("evidence_ready"):
        return "end"
    return "bias"


def route_after_analysis(state: ReviewGuardState) -> str:
    """P4 gate: HALT on INSUFFICIENT confidence."""
    if state.get("pipeline_status") in ("FAILED", "HALTED"):
        return "end"
    conf = state.get("confidence_result")
    if conf and conf["score"] == "INSUFFICIENT":
        return "end"
    return "report_gen"


def route_after_approval(state: ReviewGuardState) -> str:
    """P3 branching: APPROVED → finalize, REVISION → regenerate, REJECT → end."""
    status = state.get("approval_status", "PENDING")
    if status == "APPROVED":
        return "finalize"
    if status == "REVISION_REQUESTED":
        return "report_gen"   # Re-run report generation with same evidence
    return "end"              # REJECTED


def route_after_error(state: ReviewGuardState) -> str:
    """Catch-all for any unexpected error state."""
    if state.get("pipeline_status") in ("FAILED", "HALTED", "COMPLETED"):
        return "end"
    return "continue"


# ── Graph Construction ─────────────────────────────────────────────────────────

def build_pipeline_graph() -> StateGraph:
    """
    Constructs and compiles the ReviewGuard AI LangGraph DAG.
    Returns a compiled graph ready for invoke() calls.
    """
    graph = StateGraph(ReviewGuardState)

    # ── Register Nodes ─────────────────────────────────────────────────────────
    graph.add_node("intake", intake_agent_node)
    graph.add_node("embedding", embedding_agent_node)
    graph.add_node("evidence", evidence_retrieval_node)
    graph.add_node("bias", bias_detection_node)
    graph.add_node("analysis", performance_analysis_node)
    graph.add_node("report_gen", report_generation_node)
    graph.add_node("explainability", explainability_node)
    graph.add_node("human_approval", human_approval_node)
    graph.add_node("finalization", finalization_node)

    # ── Entry Point ────────────────────────────────────────────────────────────
    graph.set_entry_point("intake")

    # ── Conditional Edges ──────────────────────────────────────────────────────
    graph.add_conditional_edges(
        "intake",
        route_after_intake,
        {"embedding": "embedding", "end": END},
    )

    graph.add_conditional_edges(
        "embedding",
        route_after_embedding,
        {"evidence": "evidence", "end": END},
    )

    # Evidence → Bias → Analysis (sequential after parallel data)
    graph.add_conditional_edges(
        "evidence",
        route_after_evidence,
        {"bias": "bias", "end": END},
    )

    graph.add_edge("bias", "analysis")

    graph.add_conditional_edges(
        "analysis",
        route_after_analysis,
        {"report_gen": "report_gen", "end": END},
    )

    graph.add_edge("report_gen", "explainability")
    graph.add_edge("explainability", "human_approval")

    graph.add_conditional_edges(
        "human_approval",
        route_after_approval,
        {
            "finalize": "finalization",
            "report_gen": "report_gen",   # REVISION_REQUESTED loops back
            "end": END,                   # REJECTED
        },
    )

    graph.add_edge("finalization", END)

    return graph.compile()


# Module-level singleton graph
pipeline_graph = build_pipeline_graph()
