import os
from pathlib import Path

graph_dir = Path("backend/app/ai/graph")
graph_dir.mkdir(parents=True, exist_ok=True)

# 1. nodes.py
(graph_dir / "nodes.py").write_text('''"""
Graph Nodes executing individual agents.
"""
import logging
from typing import Callable, Any
from app.ai.state.review_state import ReviewState

logger = logging.getLogger(__name__)

class GraphNodes:
    def __init__(self, intake_agent, embedding_agent, retrieval_agent):
        self.intake_agent = intake_agent
        self.embedding_agent = embedding_agent
        self.retrieval_agent = retrieval_agent

    def intake_node(self, state: ReviewState) -> Any:
        try:
            logger.info("Executing Intake Node...")
            return self.intake_agent.execute(state)
        except Exception as e:
            logger.error(f"Intake Node failed: {str(e)}")
            state.metadata.pipeline_status = "FAILED"
            state.audit.errors.append(f"Intake Node failed: {str(e)}")
            return state

    def embedding_node(self, state: ReviewState) -> Any:
        try:
            logger.info("Executing Embedding Node...")
            return self.embedding_agent.execute(state)
        except Exception as e:
            logger.error(f"Embedding Node failed: {str(e)}")
            state.metadata.pipeline_status = "FAILED"
            state.audit.errors.append(f"Embedding Node failed: {str(e)}")
            return state

    def retrieval_node(self, state: ReviewState) -> Any:
        try:
            logger.info("Executing Retrieval Node...")
            return self.retrieval_agent.execute(state)
        except Exception as e:
            logger.error(f"Retrieval Node failed: {str(e)}")
            state.metadata.pipeline_status = "FAILED"
            state.audit.errors.append(f"Retrieval Node failed: {str(e)}")
            return state
''', encoding="utf-8")

# 2. edges.py
(graph_dir / "edges.py").write_text('''"""
Graph Edges (linear flow for Phase 1).
"""
# For linear flow, edges are handled directly in the builder via add_edge
# but we can place routing logic here if branching is needed later.
pass
''', encoding="utf-8")

# 3. builder.py
(graph_dir / "builder.py").write_text('''"""
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
''', encoding="utf-8")

# 4. executor.py
(graph_dir / "executor.py").write_text('''"""
Executes the compiled LangGraph pipeline.
"""
from app.ai.state.review_state import ReviewState

class PipelineExecutor:
    def __init__(self, compiled_graph):
        self.compiled_graph = compiled_graph
        
    def invoke(self, state: ReviewState) -> ReviewState:
        """
        Invokes the graph and returns the final state.
        Handles LangGraph's output formatting.
        """
        # Langgraph invoke returns the final state dict or object
        final_state = self.compiled_graph.invoke(state)
        # Depending on Pydantic/LangGraph interaction, it might return the model or a dict.
        # If it's a dict, we parse it back, else we return it directly.
        if isinstance(final_state, dict):
            return ReviewState(**final_state)
        return final_state
''', encoding="utf-8")

# 5. graph.py
(graph_dir / "graph.py").write_text('''"""
Facade for the Graph sub-system.
"""
from .builder import PipelineBuilder
from .executor import PipelineExecutor
from .nodes import GraphNodes

class ReviewGuardGraph:
    """Entry point for initializing and executing the graph."""
    def __init__(self, intake_agent, embedding_agent, retrieval_agent):
        nodes = GraphNodes(intake_agent, embedding_agent, retrieval_agent)
        builder = PipelineBuilder(nodes)
        self.compiled_graph = builder.build()
        self.executor = PipelineExecutor(self.compiled_graph)
        
    def execute(self, state) -> dict:
        # LangGraph invoke
        return self.executor.invoke(state)
''', encoding="utf-8")

# 6. __init__.py
(graph_dir / "__init__.py").write_text('''"""
Enterprise LangGraph Workflow
"""
from .builder import PipelineBuilder
from .executor import PipelineExecutor
from .nodes import GraphNodes
from .graph import ReviewGuardGraph
''', encoding="utf-8")

print("Created LangGraph Pipeline files")
