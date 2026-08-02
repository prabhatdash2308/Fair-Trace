import os
import pytest
import asyncio
from tests.e2e.utils.pipeline_runner import PipelineRunner
from fastapi.testclient import TestClient
from main import app

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")

@pytest.mark.asyncio
async def test_concurrent_workflows():
    """E2E Scenario 9: Concurrent Users."""
    # We use httpx AsyncClient for true concurrency in a real scenario, but with TestClient it's synchronous.
    # To test concurrency in the backend, we start multiple workflows and they run in background tasks.
    
    auth_headers = {"Authorization": "Bearer admin_token"}
    filepath = os.path.join(FIXTURES_DIR, "average_employee.pdf")
    
    # Use TestClient directly
    client = TestClient(app)
    runner = PipelineRunner(client, auth_headers)
    
    # 1. Upload 5 documents
    doc_ids = []
    for _ in range(3): # Limit to 3 to keep test fast
        doc_id = runner.upload_document(filepath)
        runner.extract_document(doc_id)
        doc_ids.append(doc_id)
        
    # 2. Start 3 workflows concurrently
    workflow_ids = []
    for doc_id in doc_ids:
        wid = runner.start_workflow(doc_id)
        workflow_ids.append(wid)
        
    # 3. Wait for all to reach WAITING_APPROVAL
    import time
    start = time.time()
    while time.time() - start < 30:
        all_ready = True
        for wid in workflow_ids:
            res = client.get(f"/api/v1/workflows/{wid}", headers=auth_headers)
            if res.json()["status"] != "WAITING_APPROVAL":
                all_ready = False
                break
        if all_ready:
            break
        time.sleep(1)
        
    # Verify all are waiting
    for wid in workflow_ids:
        res = client.get(f"/api/v1/workflows/{wid}", headers=auth_headers)
        assert res.json()["status"] == "WAITING_APPROVAL"
        
    # 4. Approve and resume all
    for wid in workflow_ids:
        runner.approve_workflow(wid, "LGTM")
        runner.resume_workflow(wid)
        
    # 5. Wait for all COMPLETED
    start = time.time()
    while time.time() - start < 30:
        all_done = True
        for wid in workflow_ids:
            res = client.get(f"/api/v1/workflows/{wid}", headers=auth_headers)
            if res.json()["status"] != "COMPLETED":
                all_done = False
                break
        if all_done:
            break
        time.sleep(1)
        
    # Verify all are completed
    for wid in workflow_ids:
        res = client.get(f"/api/v1/workflows/{wid}", headers=auth_headers)
        assert res.json()["status"] == "COMPLETED"
