from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
import structlog
import uuid

from dependencies import get_current_user
from models.db.user import User
from app.ai.agents.bias.service import BiasAnalysisService

router = APIRouter(prefix="/bias", tags=["Bias Detection Agent"])
logger = structlog.get_logger(__name__)

@router.post("/analyze", response_model=Dict[str, Any])
async def run_bias_analysis(
    payload: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Executes the Bias Detection Agent independently of the graph for testing/API usage."""
    
    context_bundle = payload.get("context_bundle")
    performance_analysis = payload.get("performance_analysis")
    
    if not context_bundle:
        raise HTTPException(status_code=400, detail="context_bundle is required")
    if not performance_analysis:
        raise HTTPException(status_code=400, detail="performance_analysis is required")
        
    state = {
        "execution_id": str(uuid.uuid4()),
        "context_bundle": context_bundle,
        "performance_analysis": performance_analysis,
        "user_id": str(current_user.id),
        "organization_id": getattr(current_user, "organization_id", None)
    }
    
    try:
        result = await BiasAnalysisService.analyze_context(state)
        return result
    except Exception as e:
        logger.error("api_bias_analysis_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def get_bias_health():
    """Returns the operational health of the Bias agent."""
    return BiasAnalysisService.get_health()

@router.get("/version")
async def get_bias_version():
    """Returns the active version config of the Bias agent."""
    health = BiasAnalysisService.get_health()
    return {
        "agent_version": "1.0",
        "prompt_version": health["prompt_version"],
        "prompt_hash": health["prompt_hash"]
    }
