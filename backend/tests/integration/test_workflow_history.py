import pytest
from app.workflows.history_service import HistoryService
from unittest.mock import MagicMock

def test_history_service_log_event():
    mock_db = MagicMock()
    
    history = HistoryService.log_event(
        db=mock_db,
        workflow_id="wf-123",
        event="workflow_paused",
        trigger="HumanApprovalNode",
        previous_status="RUNNING",
        new_status="WAITING_APPROVAL"
    )
    
    assert history.workflow_id == "wf-123"
    assert history.event == "workflow_paused"
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
