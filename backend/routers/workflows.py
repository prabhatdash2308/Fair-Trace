from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import Dict, Any, List
from sqlalchemy.orm import Session
import uuid

from dependencies import get_current_user, get_db
from models.db.user import User
from app.workflows.workflow_service import WorkflowService
from app.workflows.approval_service import ApprovalService
from app.workflows.history_service import HistoryService
from models.db.workflow import WorkflowExecution, ApprovalRequest

router = APIRouter(prefix="/workflows", tags=["Workflows"])

@router.post("/start")
async def start_workflow(
    payload: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Starts the LangGraph enterprise AI pipeline (Stub for orchestration hook)."""
    return {"status": "started", "workflow_id": str(uuid.uuid4())}

@router.post("/{workflow_id}/decision")
async def make_decision(
    workflow_id: str,
    payload: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Reviewer submits a decision (approved, rejected, revision)."""
    decision = payload.get("decision")
    comment = payload.get("comment", "")
    
    if not decision:
        raise HTTPException(status_code=400, detail="Decision is required.")
        
    try:
        # Save decision
        ApprovalService.process_decision(
            db=db,
            workflow_id=workflow_id,
            reviewer=current_user,
            decision=decision,
            comment=comment,
            execution_id="mock-exec-id",
            snapshot={}
        )
        
        # Unpause graph
        WorkflowService.resume_workflow(
            db=db,
            workflow_id=workflow_id,
            actor=current_user.id,
            decision=decision
        )
        return {"status": "success", "decision": decision}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/pending")
async def get_pending(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return []

@router.get("/me")
async def get_my_workflows(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return []

@router.get("/statistics")
async def get_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return {"total": 0, "pending": 0, "approved": 0}

@router.get("/history/{workflow_id}")
async def get_workflow_history(
    workflow_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return []

@router.get("/{workflow_id}/checkpoint")
async def get_workflow_checkpoint(
    workflow_id: str,
    current_user: User = Depends(get_current_user)
):
    return {}
