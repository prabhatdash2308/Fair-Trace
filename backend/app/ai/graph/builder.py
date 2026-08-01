"""
Constructs and compiles the LangGraph StateGraph.
"""
from langgraph.graph import StateGraph, END
from app.ai.state.review_state import ReviewState
from .nodes import GraphNodes

class PipelineBuilder:
    def __init__(self, nodes: GraphNodes):
        self.nodes = nodes
        self.workflow = StateGraph(ReviewState)
        
    def build(self):
        """Constructs a linear pipeline: Intake -> Embedding -> Retrieval"""
        
        # Add Nodes
        self.workflow.add_node("intake", self.nodes.intake_node)
        self.workflow.add_node("embedding", self.nodes.embedding_node)
        self.workflow.add_node("retrieval", self.nodes.retrieval_node)
        
        # Add Edges
        self.workflow.set_entry_point("intake")
        self.workflow.add_edge("intake", "embedding")
        self.workflow.add_edge("embedding", "retrieval")
        self.workflow.add_edge("retrieval", END)
        
        return self.workflow.compile()
