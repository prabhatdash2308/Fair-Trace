from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import Dict, Any, List
from sqlalchemy.orm import Session

from dependencies import get_current_user, get_db
from models.db.user import User
from app.export.service import ExportService
from models.db.export import ExportStatus

router = APIRouter(prefix="/export", tags=["Export"])

@router.post("/{format_type}/{workflow_id}")
async def start_export(
    format_type: str,
    workflow_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if format_type not in ["pdf", "html"]:
        raise HTTPException(status_code=400, detail="Invalid export format")
        
    try:
        export_record = ExportService.generate_export(
            db=db,
            workflow_id=workflow_id,
            actor_id=current_user.id,
            format_type=format_type
        )
        return {"status": "success", "export_id": export_record.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Export rendering failed")

@router.get("/download/{export_id}")
async def download_export(
    export_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        url = ExportService.get_download_url(db=db, export_id=export_id, actor_id=current_user.id)
        return {"download_url": url}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/history")
async def get_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return []

@router.get("/health")
async def export_health():
    return {"status": "healthy"}
