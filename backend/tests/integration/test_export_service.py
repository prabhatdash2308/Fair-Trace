import pytest
from unittest.mock import MagicMock
from app.export.service import ExportService
from models.db.workflow import WorkflowExecution, WorkflowStatus
from models.db.export import ExportStatus

def test_export_service_validation_fails():
    mock_db = MagicMock()
    wf = WorkflowExecution(id="wf-1", status=WorkflowStatus.RUNNING)
    mock_db.query().filter().first.return_value = wf
    
    with pytest.raises(ValueError, match="Cannot export workflow"):
        ExportService.generate_export(
            db=mock_db,
            workflow_id="wf-1",
            actor_id="user-1",
            format_type="pdf"
        )

def test_export_service_success():
    mock_db = MagicMock()
    wf = WorkflowExecution(id="wf-1", execution_id="exec-1", status=WorkflowStatus.APPROVED)
    mock_db.query().filter().first.return_value = wf
    
    export = ExportService.generate_export(
        db=mock_db,
        workflow_id="wf-1",
        actor_id="user-1",
        format_type="html"
    )
    
    assert export.workflow_id == "wf-1"
    assert export.status == ExportStatus.READY
    assert export.signature is not None
    assert export.storage_path.endswith(".html")
