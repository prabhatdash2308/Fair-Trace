import os
from pathlib import Path

def write_file(path_str, content):
    p = Path(path_str)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")

graph_content = '''"""
Facade for the Enterprise Graph sub-system.
"""
from typing import AsyncGenerator, Generator
from .builder import PipelineBuilder
from .executor import PipelineExecutor
from .nodes import GraphNodes
from app.ai.state.review_state import ReviewState

class ReviewGuardGraph:
    """Entry point for initializing and executing the enterprise graph."""
    def __init__(
        self, 
        intake_agent, 
        embedding_agent, 
        retrieval_agent,
        bias_agent,
        analysis_agent,
        explainability_agent,
        report_agent,
        approval_agent,
        finalization_agent
    ):
        nodes = GraphNodes(
            intake=intake_agent, 
            embedding=embedding_agent, 
            retrieval=retrieval_agent,
            bias=bias_agent,
            analysis=analysis_agent,
            explainability=explainability_agent,
            report=report_agent,
            approval=approval_agent,
            finalization=finalization_agent
        )
        builder = PipelineBuilder(nodes)
        self.compiled_graph = builder.build()
        self.executor = PipelineExecutor(self.compiled_graph)
        
    def invoke(self, state: ReviewState, thread_id: str = "default") -> ReviewState:
        return self.executor.invoke(state, thread_id)

    async def ainvoke(self, state: ReviewState, thread_id: str = "default") -> ReviewState:
        return await self.executor.ainvoke(state, thread_id)
        
    def stream(self, state: ReviewState, thread_id: str = "default") -> Generator:
        return self.executor.stream(state, thread_id)
        
    async def astream(self, state: ReviewState, thread_id: str = "default") -> AsyncGenerator:
        return self.executor.astream(state, thread_id)
'''

write_file("backend/app/ai/graph/graph.py", graph_content)
print("Updated graph.py successfully.")
