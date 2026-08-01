"""
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
