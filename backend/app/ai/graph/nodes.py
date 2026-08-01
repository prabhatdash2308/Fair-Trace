"""
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
