from typing import Dict, Any, Optional
from pydantic import BaseModel
import datetime

class BaseGraphEvent(BaseModel):
    execution_id: str
    timestamp: str = ""

    def __init__(self, **data):
        super().__init__(**data)
        if not self.timestamp:
            self.timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

class GraphStarted(BaseGraphEvent):
    pass

class GraphCompleted(BaseGraphEvent):
    pass

class GraphFailed(BaseGraphEvent):
    error: str

class NodeStarted(BaseGraphEvent):
    node_name: str

class NodeCompleted(BaseGraphEvent):
    node_name: str
    duration_ms: int
    status: str = "completed"

class NodeFailed(BaseGraphEvent):
    node_name: str
    error: str

class NodeInterrupted(BaseGraphEvent):
    node_name: str
    reason: str

class NodeResumed(BaseGraphEvent):
    node_name: str

class NodeRetried(BaseGraphEvent):
    node_name: str
    attempt: int
