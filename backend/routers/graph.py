from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
import structlog
import uuid

from dependencies import get_db, get_current_user
from models.db.user import User
from config import Settings, get_settings
from app.ai.graph.executor import GraphExecutor
from app.ai.graph.models import GraphRunRequest, GraphStatusResponse
from app.ai.graph.registry import NodeRegistry
from app.ai.graph.exceptions import GraphExecutionError, ResumeError

router = APIRouter(prefix="/graph", tags=["Graph Workflow"])
logger = structlog.get_logger(__name__)

@router.post("/run", response_model=Dict[str, Any])
async def start_graph(
    request: GraphRunRequest,
    settings: Settings = Depends(get_settings),
    current_user: User = Depends(get_current_user)
):
    """Starts a new LangGraph execution for the document."""
    execution_id = str(uuid.uuid4())
    state = {
        "execution_id": execution_id,
        "document_id": request.document_id,
        "organization_id": getattr(current_user, "organization_id", None),
        "user_id": str(current_user.id),
        "context_bundle": request.context_bundle
    }
    
    try:
        # Await graph completion or suspension
        result = await GraphExecutor.run(execution_id, state)
        
        # If interrupted, result might not contain the final state, we query status
        status_res = await GraphExecutor.get_status(execution_id)
        
        return {
            "execution_id": execution_id,
            "graph_status": status_res
        }
    except GraphExecutionError as e:
        logger.error("graph_run_failed", execution_id=execution_id, error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/resume/{execution_id}", response_model=Dict[str, Any])
async def resume_graph(
    execution_id: str,
    state_update: Dict[str, Any],
    settings: Settings = Depends(get_settings),
    current_user: User = Depends(get_current_user)
):
    """Resumes a suspended graph execution."""
    try:
        result = await GraphExecutor.resume(execution_id, state_update)
        status_res = await GraphExecutor.get_status(execution_id)
        
        return {
            "execution_id": execution_id,
            "graph_status": status_res
        }
    except ResumeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except GraphExecutionError as e:
        logger.error("graph_resume_failed", execution_id=execution_id, error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{execution_id}", response_model=Dict[str, Any])
async def get_graph_status(
    execution_id: str,
    current_user: User = Depends(get_current_user)
):
    """Retrieves current graph status."""
    return await GraphExecutor.get_status(execution_id)

@router.get("/health", response_model=Dict[str, Any])
async def get_graph_health():
    """Graph infrastructure health."""
    nodes = NodeRegistry.list_nodes()
    return {
        "graph": "healthy",
        "nodes": len(nodes),
        "checkpointer": "MemorySaver",
        "interrupts": True,
        "events": True,
        "telemetry": True,
        "compiled": True,
        "registered_nodes": [name for name in nodes.keys()]
    }
