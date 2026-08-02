from abc import ABC, abstractmethod
from app.ai.graph.state import ReviewState
from app.ai.graph.models import NodeResult
from app.ai.graph.exceptions import NodeExecutionError

class BaseNode(ABC):
    """Enterprise Base Node. Standardizes execution, validation, and lifecycle hooks."""
    
    async def validate(self, state: ReviewState):
        """Validate state before execution. Raises NodeExecutionError if invalid."""
        pass
        
    async def before(self, state: ReviewState):
        """Pre-execution hook."""
        pass
        
    async def after(self, state: ReviewState, result: NodeResult):
        """Post-execution hook."""
        pass
        
    @abstractmethod
    async def execute(self, state: ReviewState) -> NodeResult:
        """Core execution logic. Must return a NodeResult."""
        pass
        
    async def run(self, state: ReviewState) -> NodeResult:
        """The entrypoint called by LangGraph."""
        await self.validate(state)
        await self.before(state)
        result = await self.execute(state)
        await self.after(state, result)
        return result
