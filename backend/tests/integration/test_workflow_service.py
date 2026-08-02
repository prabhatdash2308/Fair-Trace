import pytest
from unittest.mock import MagicMock
from app.workflows.workflow_service import WorkflowService
from models.db.workflow import WorkflowExecution, WorkflowStatus

def test_workflow_service_pause():
    mock_db = MagicMock()
    mock_db.query().filter().first.return_value = None
    
    wf = WorkflowService.pause_workflow(
        db=mock_db,
        workflow_id="wf-123",
        execution_id="exec-123",
        node="approval_node",
        checkpoint_id="cp-123"
    )
    
    assert wf.status == WorkflowStatus.WAITING_APPROVAL
    assert wf.current_node == "approval_node"
    assert wf.paused_at is not None

def test_workflow_service_resume():
    mock_db = MagicMock()
    wf = WorkflowExecution(id="wf-123", status=WorkflowStatus.WAITING_APPROVAL)
    mock_db.query().filter().first.return_value = wf
    
    result = WorkflowService.resume_workflow(
        db=mock_db,
        workflow_id="wf-123",
        actor="user-123",
        decision="approved"
    )
    
    assert result is True
    assert wf.status == WorkflowStatus.APPROVED
    assert wf.paused_at is None
