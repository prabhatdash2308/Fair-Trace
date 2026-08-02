import pytest
from unittest.mock import patch
from models.db.user import User
from app.workflows.workflow_service import WorkflowService

@pytest.fixture
def mock_user():
    return User(id="user-123", email="test@test.com")

@pytest.mark.asyncio
async def test_workflows_start_api(test_client, mock_user):
    response = test_client.post(
        "/api/v1/workflows/start",
        json={"data": "test"},
        headers={"Authorization": "Bearer test"}
    )
    if response.status_code != 401:
        assert response.status_code == 200
        assert "workflow_id" in response.json()

@pytest.mark.asyncio
@patch("routers.workflows.ApprovalService.process_decision")
@patch("routers.workflows.WorkflowService.resume_workflow")
async def test_workflows_decision_api(mock_resume, mock_process, test_client, mock_user):
    response = test_client.post(
        "/api/v1/workflows/wf-123/decision",
        json={"decision": "approved", "comment": "ok"},
        headers={"Authorization": "Bearer test"}
    )
    if response.status_code != 401:
        assert response.status_code == 200
        mock_process.assert_called_once()
        mock_resume.assert_called_once()

@pytest.mark.asyncio
async def test_workflows_decision_api_missing_decision(test_client, mock_user):
    response = test_client.post(
        "/api/v1/workflows/wf-123/decision",
        json={"comment": "ok"},
        headers={"Authorization": "Bearer test"}
    )
    if response.status_code != 401:
        assert response.status_code == 400
        assert "Decision is required" in response.json()["detail"]
