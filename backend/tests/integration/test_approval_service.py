import pytest
from unittest.mock import MagicMock
from app.workflows.approval_service import ApprovalService
from models.db.workflow import ApprovalRequest, ApprovalStatus
from models.db.user import User

def test_approval_service_process_decision():
    mock_db = MagicMock()
    request = ApprovalRequest(workflow_id="wf-1", status=ApprovalStatus.PENDING)
    mock_db.query().filter().first.return_value = request
    
    user = User(id="u1", role="manager")
    
    result = ApprovalService.process_decision(
        db=mock_db,
        workflow_id="wf-1",
        reviewer=user,
        decision="approved",
        comment="Looks good",
        execution_id="exec-1",
        snapshot={}
    )
    
    assert result.status == ApprovalStatus.APPROVED
    assert result.decision == "approved"
    assert result.decision_reason == "Looks good"
    mock_db.commit.assert_called_once()
    
def test_approval_service_unauthorized():
    mock_db = MagicMock()
    request = ApprovalRequest(workflow_id="wf-1", status=ApprovalStatus.PENDING, reviewer_id="u2")
    mock_db.query().filter().first.return_value = request
    
    user = User(id="u1", role="user") # Not admin, not the designated reviewer
    
    with pytest.raises(ValueError, match="Unauthorized"):
        ApprovalService.process_decision(
            db=mock_db,
            workflow_id="wf-1",
            reviewer=user,
            decision="approved",
            comment="",
            execution_id="exec-1",
            snapshot={}
        )
