import os
import pytest
from tests.e2e.utils.pipeline_runner import PipelineRunner

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")

@pytest.fixture
def runner(api_client, auth_headers):
    return PipelineRunner(api_client, auth_headers)

def test_happy_path_excellent_employee(runner):
    """E2E Scenario 1: Excellent employee review."""
    filepath = os.path.join(FIXTURES_DIR, "excellent_employee.pdf")
    
    # 1. Upload
    doc_id = runner.upload_document(filepath)
    assert doc_id is not None
    
    # 2. Extract
    runner.extract_document(doc_id)
    
    # 3. Graph
    workflow_id = runner.start_workflow(doc_id)
    assert workflow_id is not None
    
    runner.wait_for_status(workflow_id, "WAITING_APPROVAL")
    
    # 4. Approve
    runner.approve_workflow(workflow_id, "Approved")
    runner.resume_workflow(workflow_id)
    runner.wait_for_status(workflow_id, "COMPLETED")
    
    # 5. Export
    export_id = runner.export_pdf(workflow_id)
    url = runner.get_download_url(export_id)
    assert "/api/v1/export/download" in url

def test_biased_employee_review(runner):
    """E2E Scenario 3: Biased review."""
    filepath = os.path.join(FIXTURES_DIR, "biased_review.pdf")
    
    doc_id = runner.upload_document(filepath)
    runner.extract_document(doc_id)
    workflow_id = runner.start_workflow(doc_id)
    
    runner.wait_for_status(workflow_id, "WAITING_APPROVAL")
    
    # Check that state contains bias
    state = runner.get_workflow_state(workflow_id)
    assert state.get("bias_analysis", {}).get("bias_detected") is True
    
    # Complete
    runner.approve_workflow(workflow_id, "Approved with notes")
    runner.resume_workflow(workflow_id)
    runner.wait_for_status(workflow_id, "COMPLETED")

def test_corrupt_pdf(runner):
    """E2E Scenario 4: Corrupt PDF parser failure."""
    filepath = os.path.join(FIXTURES_DIR, "corrupt_document.pdf")
    # Will fail during upload or extract
    with pytest.raises(Exception):
        doc_id = runner.upload_document(filepath)
        runner.extract_document(doc_id)
