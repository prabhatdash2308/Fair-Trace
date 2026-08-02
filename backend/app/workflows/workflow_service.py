from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from models.db.workflow import WorkflowExecution, WorkflowStatus
from models.db.user import User
from app.workflows.history_service import HistoryService
from app.workflows.checkpoint_service import CheckpointService

class WorkflowService:
    @staticmethod
    def pause_workflow(
        db: Session,
        workflow_id: str,
        execution_id: str,
        node: str,
        checkpoint_id: str
    ) -> WorkflowExecution:
        workflow = db.query(WorkflowExecution).filter(WorkflowExecution.id == workflow_id).first()
        if not workflow:
            # Mock fallback
            workflow = WorkflowExecution(id=workflow_id, execution_id=execution_id, owner_id="system")
            db.add(workflow)
            
        previous_status = workflow.status.value if isinstance(workflow.status, WorkflowStatus) else workflow.status
        workflow.status = WorkflowStatus.WAITING_APPROVAL
        workflow.current_node = node
        workflow.checkpoint_id = checkpoint_id
        
        import datetime
        workflow.paused_at = datetime.datetime.utcnow()
        
        db.commit()
        db.refresh(workflow)
        
        HistoryService.log_event(
            db=db,
            workflow_id=workflow_id,
            event="workflow_paused",
            trigger="HumanApprovalNode",
            node=node,
            previous_status=previous_status,
            new_status=WorkflowStatus.WAITING_APPROVAL.value,
            execution_id=execution_id,
            checkpoint_id=checkpoint_id
        )
        return workflow

    @staticmethod
    def resume_workflow(
        db: Session,
        workflow_id: str,
        actor: str,
        decision: str
    ) -> bool:
        workflow = db.query(WorkflowExecution).filter(WorkflowExecution.id == workflow_id).first()
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found.")
            
        if workflow.status != WorkflowStatus.WAITING_APPROVAL:
            raise ValueError(f"Workflow {workflow_id} is not waiting for approval.")
            
        previous_status = workflow.status.value if isinstance(workflow.status, WorkflowStatus) else workflow.status
        
        # State machine transition
        if decision == "approved":
            workflow.status = WorkflowStatus.APPROVED
        elif decision == "rejected":
            workflow.status = WorkflowStatus.REJECTED
        elif decision == "revision":
            workflow.status = WorkflowStatus.REVISION_REQUESTED
        else:
            raise ValueError(f"Unknown decision {decision}")
            
        # Un-pause
        workflow.paused_at = None
        db.commit()
        
        HistoryService.log_event(
            db=db,
            workflow_id=workflow_id,
            event="workflow_resumed",
            trigger="HumanDecision",
            previous_status=previous_status,
            new_status=workflow.status.value if isinstance(workflow.status, WorkflowStatus) else workflow.status,
            actor=actor,
            execution_id=workflow.execution_id,
            checkpoint_id=workflow.checkpoint_id,
            details={"decision": decision}
        )
        
        # Resume LangGraph thread
        if workflow.graph_thread_id:
            # LangGraph Command(resume=decision) is called externally by orchestrator via graph.invoke()
            pass
            
        return True
