"""
Constructs and compiles the Enterprise LangGraph StateGraph.
"""
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from app.ai.state.review_state import ReviewState
from .nodes import GraphNodes
from . import edges

class PipelineBuilder:
    def __init__(self, nodes: GraphNodes):
        self.nodes = nodes
        self.workflow = StateGraph(ReviewState)
        self.memory = MemorySaver()
        
    def build(self):
        """Constructs the Enterprise Workflow pipeline."""
        
        # Add Nodes
        self.workflow.add_node("intake", self.nodes.intake_node)
        self.workflow.add_node("embedding", self.nodes.embedding_node)
        self.workflow.add_node("evidence_retrieval", self.nodes.evidence_retrieval_node)
        self.workflow.add_node("bias_detection", self.nodes.bias_detection_node)
        self.workflow.add_node("performance_analysis", self.nodes.performance_analysis_node)
        self.workflow.add_node("explainability", self.nodes.explainability_node)
        self.workflow.add_node("report_generation", self.nodes.report_generation_node)
        self.workflow.add_node("human_approval", self.nodes.human_approval_node)
        self.workflow.add_node("finalization", self.nodes.finalization_node)
        self.workflow.add_node("retry_node", self.nodes.retry_node)
        
        self.workflow.set_entry_point("intake")
        
        # Add Conditional Edges
        self.workflow.add_conditional_edges("intake", edges.route_after_intake)
        self.workflow.add_conditional_edges("embedding", edges.route_after_embedding)
        self.workflow.add_conditional_edges("evidence_retrieval", edges.route_after_retrieval)
        self.workflow.add_conditional_edges("bias_detection", edges.route_after_bias)
        self.workflow.add_conditional_edges("performance_analysis", edges.route_after_analysis)
        self.workflow.add_conditional_edges("explainability", edges.route_after_explainability)
        self.workflow.add_conditional_edges("report_generation", edges.route_after_report)
        
        self.workflow.add_conditional_edges(
            "human_approval", 
            edges.decision_router,
            {
                "finalization": "finalization",
                "report_generation": "report_generation",
                "retry_node": "retry_node",
                "END": END
            }
        )
        
        self.workflow.add_conditional_edges("retry_node", edges.retry_router, {
            "intake": "intake",
            "embedding": "embedding",
            "evidence_retrieval": "evidence_retrieval",
            "bias_detection": "bias_detection",
            "performance_analysis": "performance_analysis",
            "analysis": "performance_analysis", # fallback
            "explainability": "explainability",
            "report_generation": "report_generation",
            "report": "report_generation", # fallback
            "human_approval": "human_approval",
            "END": END
        })
        self.workflow.add_edge("finalization", END)
        
        # Compile with Checkpointing and Interrupt
        return self.workflow.compile(
            checkpointer=self.memory,
            interrupt_after=["human_approval"]
        )
