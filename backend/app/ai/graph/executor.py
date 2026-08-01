"""
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
