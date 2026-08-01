"""
Executes the compiled LangGraph pipeline supporting enterprise streaming and interrupts.
"""
from typing import AsyncGenerator, Generator
from app.ai.state.review_state import ReviewState

class PipelineExecutor:
    def __init__(self, compiled_graph):
        self.compiled_graph = compiled_graph
        
    def invoke(self, state: ReviewState, thread_id: str = "default") -> ReviewState:
        config = {"configurable": {"thread_id": thread_id}}
        final_state = self.compiled_graph.invoke(state, config=config)
        if isinstance(final_state, dict):
            return ReviewState(**final_state)
        return final_state

    async def ainvoke(self, state: ReviewState, thread_id: str = "default") -> ReviewState:
        config = {"configurable": {"thread_id": thread_id}}
        final_state = await self.compiled_graph.ainvoke(state, config=config)
        if isinstance(final_state, dict):
            return ReviewState(**final_state)
        return final_state
        
    def stream(self, state: ReviewState, thread_id: str = "default") -> Generator:
        config = {"configurable": {"thread_id": thread_id}}
        for output in self.compiled_graph.stream(state, config=config):
            yield output

    async def astream(self, state: ReviewState, thread_id: str = "default") -> AsyncGenerator:
        config = {"configurable": {"thread_id": thread_id}}
        async for output in self.compiled_graph.astream(state, config=config):
            yield output
