import os
from pathlib import Path

def write_file(path_str, content):
    p = Path(path_str)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")

nodes_content = '''"""
Graph Nodes executing individual agents for the Enterprise Workflow.
"""
import logging
from typing import Any
from app.ai.state.review_state import ReviewState, PipelineStatus
from app.ai.base.exceptions import StateValidationError, RetryExceededError

logger = logging.getLogger(__name__)

class GraphNodes:
    def __init__(self, **agents):
        self.agents = agents

    def _execute_agent(self, agent_name: str, state: ReviewState) -> ReviewState:
        agent = self.agents.get(agent_name)
        if not agent:
            raise ValueError(f"Agent {agent_name} not found.")
            
        state.execution.current_step = agent_name
        try:
            logger.info(f"Executing {agent_name}...")
            return agent.execute(state)
        except StateValidationError as e:
            logger.error(f"{agent_name} validation failed: {str(e)}")
            state.metadata.pipeline_status = PipelineStatus.FAILED
            state.audit.errors.append(f"{agent_name} StateValidationError: {str(e)}")
            state.execution.failed_steps.append(agent_name)
            return state
        except RetryExceededError as e:
            logger.error(f"{agent_name} retry exceeded: {str(e)}")
            state.audit.errors.append(f"{agent_name} RetryExceededError: {str(e)}")
            state.execution.failed_steps.append(agent_name)
            # Route to retry node
            state.metadata.pipeline_status = "NEEDS_RETRY"
            return state
        except Exception as e:
            logger.error(f"{agent_name} unexpected failure: {str(e)}")
            state.metadata.pipeline_status = PipelineStatus.FAILED
            state.audit.errors.append(f"{agent_name} Exception: {str(e)}")
            state.execution.failed_steps.append(agent_name)
            return state

    def intake_node(self, state: ReviewState) -> ReviewState:
        return self._execute_agent("intake", state)

    def embedding_node(self, state: ReviewState) -> ReviewState:
        return self._execute_agent("embedding", state)

    def evidence_retrieval_node(self, state: ReviewState) -> ReviewState:
        return self._execute_agent("retrieval", state)

    def bias_detection_node(self, state: ReviewState) -> ReviewState:
        return self._execute_agent("bias", state)

    def performance_analysis_node(self, state: ReviewState) -> ReviewState:
        return self._execute_agent("analysis", state)

    def explainability_node(self, state: ReviewState) -> ReviewState:
        return self._execute_agent("explainability", state)

    def report_generation_node(self, state: ReviewState) -> ReviewState:
        return self._execute_agent("report", state)

    def human_approval_node(self, state: ReviewState) -> ReviewState:
        return self._execute_agent("approval", state)

    def finalization_node(self, state: ReviewState) -> ReviewState:
        return self._execute_agent("finalization", state)

    def retry_node(self, state: ReviewState) -> ReviewState:
        logger.warning(f"Entering Retry Node. Current count: {state.execution.retry_count}")
        state.execution.retry_count += 1
        if state.execution.retry_count > 3:
            logger.error("Max graph retries exceeded.")
            state.metadata.pipeline_status = PipelineStatus.FAILED
        else:
            state.metadata.pipeline_status = PipelineStatus.IN_PROGRESS
        return state
'''

edges_content = '''"""
Graph Edges defining conditional routing for the Enterprise Workflow.
"""
from app.ai.state.review_state import ReviewState, PipelineStatus

def default_router(state: ReviewState, next_node: str) -> str:
    if state.metadata.pipeline_status == PipelineStatus.FAILED:
        return "END"
    if state.metadata.pipeline_status == "NEEDS_RETRY":
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
    return default_router(state, "explainability")

def route_after_explainability(state: ReviewState) -> str:
    return default_router(state, "report_generation")

def route_after_report(state: ReviewState) -> str:
    return default_router(state, "human_approval")

def decision_router(state: ReviewState) -> str:
    if state.metadata.pipeline_status == PipelineStatus.FAILED:
        return "END"
    if state.metadata.pipeline_status == "NEEDS_RETRY":
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
'''

builder_content = '''"""
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
        
        self.workflow.add_conditional_edges("retry_node", edges.retry_router)
        self.workflow.add_edge("finalization", END)
        
        # Compile with Checkpointing and Interrupt
        return self.workflow.compile(
            checkpointer=self.memory,
            interrupt_after=["human_approval"]
        )
'''

executor_content = '''"""
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
'''

finalization_agent_content = '''"""
Finalization Agent for finalizing the review pipeline state.
"""
import time
import datetime
from app.ai.base.base_agent import BaseAgent
from app.ai.base.execution_context import ExecutionContext
from app.ai.state.review_state import ReviewState, PipelineStatus
from app.ai.base.exceptions import StateValidationError

class FinalizationAgent(BaseAgent):
    def __init__(self, name="FinalizationAgent", max_retries=1):
        super().__init__(name=name, max_retries=max_retries)

    def _validate_before_process(self, state: ReviewState) -> None:
        if state.approval.approval_status != "APPROVED":
            raise StateValidationError("Cannot finalize unless approved.")

    def _process(self, state: ReviewState, context: ExecutionContext) -> ReviewState:
        self._validate_before_process(state)
        
        start_time = time.perf_counter()
        
        state.metadata.pipeline_status = PipelineStatus.COMPLETED
        state.report.status = "finalized"
        
        latency = int((time.perf_counter() - start_time) * 1000)
        state.execution.completed_steps.append(self.name)
        state.audit.agent_logs.append(f"[{self.name}] Pipeline Finalized in {latency}ms.")
        return state
'''

write_file("backend/app/ai/graph/nodes.py", nodes_content)
write_file("backend/app/ai/graph/edges.py", edges_content)
write_file("backend/app/ai/graph/builder.py", builder_content)
write_file("backend/app/ai/graph/executor.py", executor_content)
write_file("backend/app/ai/agents/finalization_agent.py", finalization_agent_content)
print("Graph files generated successfully.")
