from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
import structlog
import uuid

from dependencies import get_current_user
from models.db.user import User
from app.ai.agents.explainability.service import ExplainabilityAnalysisService

router = APIRouter(prefix="/explainability", tags=["Explainability Agent"])
logger = structlog.get_logger(__name__)

@router.post("/analyze", response_model=Dict[str, Any])
async def run_explainability_analysis(
    payload: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Executes the Explainability Agent independently of the graph."""
    
    context_bundle = payload.get("context_bundle")
    performance_analysis = payload.get("performance_analysis")
    bias_analysis = payload.get("bias_analysis")
    
    if not context_bundle:
        raise HTTPException(status_code=400, detail="context_bundle is required")
    if not performance_analysis:
        raise HTTPException(status_code=400, detail="performance_analysis is required")
    if not bias_analysis:
        raise HTTPException(status_code=400, detail="bias_analysis is required")
        
    state = {
        "execution_id": str(uuid.uuid4()),
        "context_bundle": context_bundle,
        "performance_analysis": performance_analysis,
        "bias_analysis": bias_analysis,
        "user_id": str(current_user.id),
        "organization_id": getattr(current_user, "organization_id", None)
    }
    
    try:
        result = await ExplainabilityAnalysisService.analyze_context(state)
        return result
    except Exception as e:
        logger.error("api_explainability_analysis_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def get_explainability_health():
    return ExplainabilityAnalysisService.get_health()

@router.get("/version")
async def get_explainability_version():
    health = ExplainabilityAnalysisService.get_health()
    return {
        "agent_version": "1.0",
        "prompt_version": health["prompt_version"],
        "prompt_hash": health["prompt_hash"]
    }
