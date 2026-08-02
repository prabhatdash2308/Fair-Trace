import pytest
from app.workflows.workflow_service import WorkflowService
from models.db.workflow import WorkflowExecution, WorkflowStatus
from unittest.mock import MagicMock

def test_duplicate_resume():
    mock_db = MagicMock()
    # Already approved workflow
    wf = WorkflowExecution(id="wf-123", status=WorkflowStatus.APPROVED)
    mock_db.query().filter().first.return_value = wf
    
    with pytest.raises(ValueError, match="not waiting for approval"):
        WorkflowService.resume_workflow(
            db=mock_db,
            workflow_id="wf-123",
            actor="user-123",
            decision="approved"
        )
