from typing import Dict, Any, Optional
import datetime
from sqlalchemy.orm import Session
from models.db.workflow import ApprovalRequest, ApprovalStatus
from models.db.user import User
from app.workflows.audit_service import AuditService

class ApprovalService:
    @staticmethod
    def process_decision(
        db: Session,
        workflow_id: str,
        reviewer: User,
        decision: str,
        comment: str,
        execution_id: str,
        snapshot: Dict[str, Any]
    ) -> ApprovalRequest:
        
        # In a real enterprise system, we'd fetch the active request from DB.
        request = db.query(ApprovalRequest).filter(
            ApprovalRequest.workflow_id == workflow_id,
            ApprovalRequest.status.in_([ApprovalStatus.PENDING, ApprovalStatus.IN_REVIEW])
        ).first()
        
        if not request:
            # Fallback for testing/mocking
            request = ApprovalRequest(workflow_id=workflow_id, execution_id=execution_id)
            db.add(request)
            
        if request.reviewer_id and request.reviewer_id != reviewer.id and reviewer.role != "admin":
            raise ValueError("Unauthorized: Reviewer does not own this approval workflow.")
            
        decision = decision.lower()
        if decision == "approved":
            request.status = ApprovalStatus.APPROVED
            request.approved_at = datetime.datetime.utcnow()
        elif decision == "rejected":
            request.status = ApprovalStatus.REJECTED
        elif decision == "revision":
            request.status = ApprovalStatus.REVISION_REQUESTED
            request.revision_count += 1
        else:
            raise ValueError(f"Invalid decision: {decision}")
            
        request.decision = decision
        request.decision_version = "1.0"
        request.decision_reason = comment
        request.decision_timestamp = datetime.datetime.utcnow()
        request.reviewer_snapshot = snapshot
        
        db.commit()
        db.refresh(request)
        
        AuditService.audit_decision(
            workflow_id=workflow_id,
            execution_id=execution_id,
            actor=reviewer.id,
            decision=decision,
            decision_version="1.0",
            reason=comment,
            snapshot=snapshot
        )
        
        return request
