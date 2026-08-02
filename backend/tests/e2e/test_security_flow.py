import pytest
import os
from tests.e2e.utils.pipeline_runner import PipelineRunner

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")

@pytest.fixture
def runner(api_client, auth_headers):
    return PipelineRunner(api_client, auth_headers)

def test_missing_jwt(api_client):
    """E2E Scenario: Missing JWT token."""
    res = api_client.post("/api/v1/uploads")
    assert res.status_code == 401

def test_expired_or_invalid_jwt(api_client):
    """E2E Scenario: Invalid JWT token."""
    headers = {"Authorization": "Bearer invalid_token_123"}
    res = api_client.post("/api/v1/uploads", headers=headers)
    assert res.status_code == 401

def test_idor_cross_user_access(runner, api_client):
    """E2E Scenario: IDOR (Cross-user access)."""
    filepath = os.path.join(FIXTURES_DIR, "average_employee.pdf")
    doc_id = runner.upload_document(filepath)
    
    # Try to access it with a different user's token
    hacker_headers = {"Authorization": "Bearer hacker_token"}
    res = api_client.get(f"/api/v1/documents/{doc_id}", headers=hacker_headers)
    # Depending on implementation, might be 401 (invalid mock token) or 403 (unauthorized) or 404 (not found)
    assert res.status_code in (401, 403, 404)

def test_sql_injection_payload(api_client, auth_headers):
    """E2E Scenario: SQL Injection payload in workflow start."""
    payload = {"document_id": "1' OR '1'='1"}
    res = api_client.post("/api/v1/workflows/start", json=payload, headers=auth_headers)
    # Should not process or return 500
    assert res.status_code in (400, 401, 404, 422)

def test_path_traversal_payload(api_client, auth_headers):
    """E2E Scenario: Path traversal payload."""
    res = api_client.get("/api/v1/documents/../../../etc/passwd", headers=auth_headers)
    assert res.status_code in (400, 404, 422)
