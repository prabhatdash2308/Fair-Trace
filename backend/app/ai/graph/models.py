from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import datetime

class NodeDefinition(BaseModel):
    """Dynamically registers nodes for Graph Builder discovery."""
    name: str
    version: str = "1.0"
    description: str
    node_class: type
    dependencies: List[str] = Field(default_factory=list)
    interruptable: bool = False
    retryable: bool = True

class NodeResult(BaseModel):
    """Standardized output from any executing graph node."""
    state: Dict[str, Any]  # The ReviewState diff/update
    status: str = "completed"
    events: List[Dict[str, Any]] = Field(default_factory=list)
    telemetry: Dict[str, Any] = Field(default_factory=dict)
    next_node: Optional[str] = None
    
    # Future injection points:
    token_usage: int = 0
    cost_usd: float = 0.0
    confidence_score: float = 1.0
    warnings: List[str] = Field(default_factory=list)

class GraphRunRequest(BaseModel):
    """API payload for starting the LangGraph."""
    document_id: str
    context_bundle: Dict[str, Any]  # Passes the retrieved ContextBundle payload

class GraphStatusResponse(BaseModel):
    """API payload for graph monitoring."""
    execution_id: str
    status: str
    current_node: Optional[str] = None
    started_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
