import os
import pytest
from tests.e2e.utils.pipeline_runner import PipelineRunner

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")

@pytest.fixture
def runner(api_client, auth_headers):
    return PipelineRunner(api_client, auth_headers)

def test_workflow_rejection(runner):
    """E2E Scenario 8: Reject Workflow."""
    filepath = os.path.join(FIXTURES_DIR, "average_employee.pdf")
    
    doc_id = runner.upload_document(filepath)
    runner.extract_document(doc_id)
    workflow_id = runner.start_workflow(doc_id)
    
    runner.wait_for_status(workflow_id, "WAITING_APPROVAL")
    
    # Reject it
    res = runner.api_client.post(
        f"/api/v1/workflows/{workflow_id}/approve",
        json={"comments": "Completely wrong", "decision": "REJECTED"},
        headers=runner.auth_headers
    )
    assert res.status_code == 200
    
    # Check that workflow transitions to REJECTED without continuing
    runner.resume_workflow(workflow_id)
    
    state = runner.get_workflow_state(workflow_id)
    status_res = runner.api_client.get(f"/api/v1/workflows/{workflow_id}", headers=runner.auth_headers)
    assert status_res.json()["status"] == "REJECTED"
    
def test_workflow_revision(runner):
    """E2E Scenario 10: Revision Workflow."""
    filepath = os.path.join(FIXTURES_DIR, "average_employee.pdf")
    
    doc_id = runner.upload_document(filepath)
    runner.extract_document(doc_id)
    workflow_id = runner.start_workflow(doc_id)
    
    runner.wait_for_status(workflow_id, "WAITING_APPROVAL")
    
    # Request revision
    res = runner.api_client.post(
        f"/api/v1/workflows/{workflow_id}/approve",
        json={"comments": "Fix the score", "decision": "REVISION_REQUESTED"},
        headers=runner.auth_headers
    )
    assert res.status_code == 200
    
    # Check status
    status_res = runner.api_client.get(f"/api/v1/workflows/{workflow_id}", headers=runner.auth_headers)
    assert status_res.json()["status"] == "WAITING_APPROVAL" # Remains in waiting approval technically because revision needs action, 
    # Or based on our implementation it goes back to "RUNNING" if we loop it, but we don't have a revision loop implemented in the graph. 
    # Let's verify our graph implementation actually supports REVISION. In our code, any decision other than APPROVED just goes to END or fails.
    # Actually, in Phase 11.11, REVISION_REQUESTED transitions it back to RUNNING if we handled it, otherwise it stays paused or REJECTED.
