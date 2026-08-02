from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
import structlog
import uuid

from dependencies import get_current_user
from models.db.user import User
from app.ai.agents.report.service import ReportGenerationService

router = APIRouter(prefix="/report", tags=["Report Generation"])
logger = structlog.get_logger(__name__)

@router.post("/generate", response_model=Dict[str, Any])
async def run_report_generation(
    payload: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Executes the Report Generation Agent independently of the graph."""
    
    context_bundle = payload.get("context_bundle")
    performance_analysis = payload.get("performance_analysis")
    bias_analysis = payload.get("bias_analysis")
    explainability_analysis = payload.get("explainability_analysis")
    
    if not context_bundle:
        raise HTTPException(status_code=400, detail="context_bundle is required")
    if not performance_analysis:
        raise HTTPException(status_code=400, detail="performance_analysis is required")
    if not bias_analysis:
        raise HTTPException(status_code=400, detail="bias_analysis is required")
    if not explainability_analysis:
        raise HTTPException(status_code=400, detail="explainability_analysis is required")
        
    state = {
        "execution_id": str(uuid.uuid4()),
        "context_bundle": context_bundle,
        "performance_analysis": performance_analysis,
        "bias_analysis": bias_analysis,
        "explainability_analysis": explainability_analysis,
        "user_id": str(current_user.id),
        "organization_id": getattr(current_user, "organization_id", None)
    }
    
    try:
        result = await ReportGenerationService.generate_report(state)
        return result
    except Exception as e:
        logger.error("api_report_generation_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def get_report_health():
    return ReportGenerationService.get_health()

@router.get("/version")
async def get_report_version():
    health = ReportGenerationService.get_health()
    return {
        "agent_version": "1.0",
        "prompt_version": health["prompt_version"],
        "prompt_hash": health["prompt_hash"]
    }
