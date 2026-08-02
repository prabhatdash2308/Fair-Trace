from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
import structlog
import uuid

from dependencies import get_current_user
from models.db.user import User
from app.ai.agents.performance.service import PerformanceAnalysisService

router = APIRouter(prefix="/analysis/performance", tags=["Performance Analysis Agent"])
logger = structlog.get_logger(__name__)

@router.post("", response_model=Dict[str, Any])
async def run_performance_analysis(
    payload: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Executes the Performance Analysis Agent independently of the graph for testing/API usage."""
    
    context_bundle = payload.get("context_bundle")
    if not context_bundle:
        raise HTTPException(status_code=400, detail="context_bundle is required")
        
    state = {
        "execution_id": str(uuid.uuid4()),
        "context_bundle": context_bundle,
        "user_id": str(current_user.id),
        "organization_id": getattr(current_user, "organization_id", None)
    }
    
    try:
        result = await PerformanceAnalysisService.analyze_context(state)
        return result
    except Exception as e:
        logger.error("api_performance_analysis_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def get_performance_health():
    """Returns the operational health of the agent and provider."""
    return PerformanceAnalysisService.get_health()
