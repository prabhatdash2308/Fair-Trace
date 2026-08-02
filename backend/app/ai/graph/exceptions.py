class GraphExecutionError(Exception):
    """Base exception for all LangGraph orchestration failures."""
    pass

class NodeExecutionError(GraphExecutionError):
    """Raised when an individual node fails catastrophically."""
    pass

class CheckpointError(GraphExecutionError):
    """Raised when state serialization or persistence fails."""
    pass

class ResumeError(GraphExecutionError):
    """Raised when attempting to resume a graph that is not paused or missing state."""
    pass

class CancellationError(GraphExecutionError):
    """Raised when a graph is manually cancelled via API."""
    pass

class InterruptError(GraphExecutionError):
    """Raised when a programmatic interrupt is triggered incorrectly."""
    pass
