from typing import Dict, Any, Optional
import datetime
from sqlalchemy.orm import Session
from models.db.workflow import WorkflowHistory

class HistoryService:
    @staticmethod
    def log_event(
        db: Session,
        workflow_id: str,
        event: str,
        trigger: str,
        node: Optional[str] = None,
        previous_status: Optional[str] = None,
        new_status: Optional[str] = None,
        actor: Optional[str] = None,
        duration_ms: Optional[int] = None,
        execution_id: Optional[str] = None,
        checkpoint_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> WorkflowHistory:
        
        history = WorkflowHistory(
            workflow_id=workflow_id,
            event=event,
            trigger=trigger,
            node=node,
            previous_status=previous_status,
            new_status=new_status,
            actor=actor,
            duration_ms=duration_ms,
            execution_id=execution_id,
            checkpoint_id=checkpoint_id,
            details=details or {}
        )
        db.add(history)
        db.commit()
        db.refresh(history)
        return history
