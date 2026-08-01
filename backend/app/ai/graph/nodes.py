"""
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
        if state.execution.current_step in state.execution.failed_steps:
            state.execution.failed_steps.remove(state.execution.current_step)
        if state.execution.retry_count > 3:
            logger.error("Max graph retries exceeded.")
            state.metadata.pipeline_status = PipelineStatus.FAILED
        return state
    # def dummy
        
