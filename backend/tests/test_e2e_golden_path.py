import pytest
import uuid
import time
import requests
import asyncio
import hashlib
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from config import settings
from core.database import get_db_session
from models.db.base import Base
from models.db.organization import Organization
from models.db.user import User
from models.db.workflow import WorkflowExecution, WorkflowStatus
from models.db.report import Report, ReportStatus
from models.enums import UserRole
from core.security import hash_password

# Use the real database URL, but we will create isolated data within it.
engine = create_engine(settings.database_url)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from app.ai.agents.bias_detection_agent import BiasDetectionAgent
from app.ai.agents.performance_analysis_agent import PerformanceAnalysisAgent
from app.ai.agents.explainability_agent import ExplainabilityAgent
from app.ai.agents.report_generation_agent import ReportGenerationAgent

# Mock agents to avoid real LLM calls during E2E tests
def mock_bias_process(self, state, context):
    state.bias.findings = []
    state.bias.status = "completed"
    return state

def mock_analysis_process(self, state, context):
    state.analysis.strengths = ["Technical skills"]
    state.analysis.competencies = {"Technical": 85.0}
    state.analysis.confidence_score = 90.0
    state.analysis.status = "completed"
    return state

def mock_explainability_process(self, state, context):
    state.explainability.decision_path = ["Looked at evidence", "Scored 85"]
    state.explainability.competency_explanations = {"Technical": "Good evidence"}
    state.explainability.status = "completed"
    return state

def mock_report_process(self, state, context):
    state.report.executive_summary = "Good performance"
    state.report.recommendations = ["Keep it up"]
    state.report.status = "completed"
    return state

BiasDetectionAgent._process = mock_bias_process
PerformanceAnalysisAgent._process = mock_analysis_process
ExplainabilityAgent._process = mock_explainability_process
ReportGenerationAgent._process = mock_report_process

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="module")
def setup_test_data(db_session):
    # Create isolated organization
    org = Organization(id=uuid.uuid4(), name=f"E2E_Test_Org_{uuid.uuid4().hex[:8]}")
    db_session.add(org)
    db_session.commit()
    
    password = "E2ETestPassword123!"
    hashed = hash_password(password)
    
    # Create Admin
    admin = User(
        email=f"admin_{uuid.uuid4().hex[:8]}@test.com",
        password_hash=hashed,
        full_name="E2E Admin",
        role=UserRole.ORG_ADMIN,
        organization_id=org.id,
        is_active=True
    )
    
    # Create Manager A
    manager_a = User(
        email=f"managera_{uuid.uuid4().hex[:8]}@test.com",
        password_hash=hashed,
        full_name="E2E Manager A",
        role=UserRole.MANAGER,
        organization_id=org.id,
        is_active=True
    )
    
    # Create Manager B (for auth testing)
    manager_b = User(
        email=f"managerb_{uuid.uuid4().hex[:8]}@test.com",
        password_hash=hashed,
        full_name="E2E Manager B",
        role=UserRole.MANAGER,
        organization_id=org.id,
        is_active=True
    )
    
    # Create Employee
    employee = User(
        email=f"employee_{uuid.uuid4().hex[:8]}@test.com",
        password_hash=hashed,
        full_name="E2E Employee",
        role=UserRole.EMPLOYEE,
        organization_id=org.id,
        is_active=True
    )
    
    db_session.add_all([admin, manager_a, manager_b, employee])
    db_session.commit()
    
    db_session.refresh(org)
    db_session.refresh(admin)
    db_session.refresh(manager_a)
    db_session.refresh(manager_b)
    db_session.refresh(employee)
    
    yield {
        "org": org,
        "admin": admin,
        "manager_a": manager_a,
        "manager_b": manager_b,
        "employee": employee,
        "password": password
    }
    
    # Cleanup (optional but good for test isolation, though cascading deletes are needed)
    pass

def login(client, email, password):
    res = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    if res.status_code != 200: print('ERROR', res.json()); assert res.status_code == 200, f"Login failed for {email}"
    return res.json()["access_token"]

def test_golden_path_e2e(client, setup_test_data, db_session):
    data = setup_test_data
    
    # 1. Login with different roles
    token_manager_a = login(client, data["manager_a"].email, data["password"])
    token_manager_b = login(client, data["manager_b"].email, data["password"])
    token_employee = login(client, data["employee"].email, data["password"])
    
    headers_a = {"Authorization": f"Bearer {token_manager_a}"}
    headers_b = {"Authorization": f"Bearer {token_manager_b}"}
    headers_emp = {"Authorization": f"Bearer {token_employee}"}
    
    # 2. Manager A creates a cycle
    res = client.post("/api/v1/review-cycles", headers=headers_a, json={
        "title": "2026 Annual Review Cycle",
        "start_date": "2026-01-01",
        "end_date": "2026-12-31"
    })
    assert res.status_code == 201
    cycle_id = res.json()["id"]
    
    # 2b. Transition to ACTIVE
    res_status = client.patch(f"/api/v1/review-cycles/{cycle_id}/status", headers=headers_a, json={"status": "ACTIVE"})
    assert res_status.status_code == 200
    
    # 2c. Manager A creates a Review for the employee
    res_rev = client.post("/api/v1/reviews", headers=headers_a, json={
        "review_cycle_id": cycle_id,
        "employee_id": str(data["employee"].id),
        "title": "2026 Annual Review",
        "review_period_start": "2026-01-01",
        "review_period_end": "2026-12-31"
    })
    assert res_rev.status_code == 201
    review_id = res_rev.json()["id"]
    
    # 3. Manager B tries to access Manager A's cycle/review (should fail or not see it)
    res_b = client.get(f"/api/v1/reviews/{review_id}", headers=headers_b)
    # Depending on exact RBAC, Manager B might get 403 or 404
    assert res_b.status_code in [403, 404]
    
    # Employee tries to access review
    res_emp = client.get(f"/api/v1/reviews/{review_id}", headers=headers_emp)
    # Employee should see their own review
    assert res_emp.status_code == 200
    
    # 4. Add Evidence (Manager A or Employee)
    res = client.post(f"/api/v1/reviews/{review_id}/inputs", headers=headers_emp, json={
        "input_type": "SELF_ASSESSMENT",
        "content_text": "This is a detailed self evaluation with sufficient length to pass validation. This is a detailed self evaluation with sufficient length to pass validation."
    })
    if res.status_code != 201: print('ERROR', res.json()); assert res.status_code == 201
    
    # 5. Concurrent Trigger (Idempotency check)
    import threading
    responses = []
    def trigger():
        r = client.post(f"/api/v1/reviews/{review_id}/pipeline/trigger", headers=headers_a)
        responses.append(r)
        
    t1 = threading.Thread(target=trigger)
    t2 = threading.Thread(target=trigger)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    
    # One should succeed, one should fail with 409 Conflict
    status_codes = [r.status_code for r in responses]
    assert 202 in status_codes, "At least one trigger should succeed"
    assert 409 in status_codes, "Duplicate trigger should be prevented by DB constraints"
    
    success_res = next(r for r in responses if r.status_code == 202)
    pipeline_run_id = success_res.json()["pipeline_run_id"]
    
    # 6. Wait for pipeline completion
    max_retries = 30
    completed = False
    for _ in range(max_retries):
        res = client.get(f"/api/v1/pipeline/{pipeline_run_id}/status", headers=headers_a)
        pipeline_status = res.json()["pipeline_status"]
        if pipeline_status in ["COMPLETED", "FAILED"]:
            completed = True
            assert pipeline_status == "COMPLETED"
            break
        time.sleep(1)
        
    assert completed, "Pipeline did not complete in time"
    
    # 7. Check review status is PENDING_APPROVAL
    res = client.get(f"/api/v1/reviews/{review_id}", headers=headers_a)
    assert res.json()["status"] == "PENDING_APPROVAL"
    
    # 8. Revision Flow
    res_reports = client.get("/api/v1/reports", headers=headers_a)
    reports = [r for r in res_reports.json() if r["review_id"] == review_id]
    assert len(reports) > 0, "Report should have been created"
    report_id = reports[0]["id"]
    res = client.patch(f"/api/v1/reports/{report_id}/status", headers=headers_a, json={
        "action": "REVISION_REQUESTED",
        "reason": "Please include more focus on leadership skills.",
        "idempotency_key": str(uuid.uuid4())
    })
    if res.status_code != 200: print('ERROR', res.json()); assert res.status_code == 200
    
    res = client.get(f"/api/v1/reviews/{review_id}", headers=headers_a)
    assert res.json()["status"] == "PENDING_APPROVAL"
    
    completed = False
    for _ in range(max_retries):
        res = client.get(f"/api/v1/reviews/{review_id}", headers=headers_a)
        if res.json()["status"] == "PENDING_APPROVAL":
            completed = True
            break
        time.sleep(1)
        
    assert completed, "Revision Pipeline did not complete in time"
    
    res = client.get(f"/api/v1/review-cycles/{cycle_id}", headers=headers_a)
    # 9. Manager A Approves
    res = client.patch(f"/api/v1/reports/{report_id}/status", headers=headers_a, json={
        "action": "APPROVED",
        "reason": "",
        "idempotency_key": str(uuid.uuid4())
    })
    assert res.status_code == 200
    
    # Verify report is APPROVED
    res_rep = client.get(f"/api/v1/reports/{report_id}", headers=headers_a)
    assert res_rep.json()["status"] == "APPROVED"
    
    # Verify Review is APPROVED
    res_cycle = client.get(f"/api/v1/reviews/{review_id}", headers=headers_a)
    assert res_cycle.json()["status"] == "APPROVED"
    
    # 10. Verify Immutability
    res = client.patch(f"/api/v1/reports/{report_id}/status", headers=headers_a, json={
        "action": "REJECT",
        "reason": "Changed my mind",
        "idempotency_key": str(uuid.uuid4())
    })
    assert res.status_code == 409, "Cannot change finalized report"
    
    res = client.patch(f"/api/v1/reports/{report_id}/status", headers=headers_a, json={
        "action": "REVISION_REQUESTED",
        "reason": "Changed my mind",
        "idempotency_key": str(uuid.uuid4())
    })
    assert res.status_code == 409, "Cannot revise finalized report"
    
    # 11. PDF Export Verification
    # Trigger export synchronously
    res = client.get(f"/api/v1/export/report/{report_id}/pdf", headers=headers_a)
    if res.status_code != 200: print('ERROR', res.text); assert res.status_code == 200
    assert res.headers["content-type"] == "application/pdf"
    pdf_bytes = res.content
    assert len(pdf_bytes) > 100, "PDF should not be empty"
    
    # Also verify HTML export
    res = client.get(f"/api/v1/export/report/{report_id}/html", headers=headers_a)
    assert res.status_code == 200
    assert "text/html" in res.headers["content-type"]
    assert len(res.content) > 100, "HTML should not be empty"
    
    print("Golden Path E2E Completed Successfully")

def test_agent_failures_e2e(client, setup_test_data, db_session):
    data = setup_test_data
    token_manager_a = login(client, data["manager_a"].email, data["password"])
    headers_a = {"Authorization": f"Bearer {token_manager_a}"}
    
    from app.ai.agents.performance_analysis_agent import PerformanceAnalysisAgent
    from app.ai.agents.bias_detection_agent import BiasDetectionAgent
    
    original_perf = PerformanceAnalysisAgent._process
    original_bias = BiasDetectionAgent._process
    
    # --- TEST 1: Critical Agent Failure (Performance) ---
    cycle_res = client.post("/api/v1/review-cycles", headers=headers_a, json={
        "title": "2026 Annual Review",
        "start_date": "2026-01-01",
        "end_date": "2026-12-31"
    })
    cycle_id_1 = cycle_res.json()["id"]
    
    # Transition to ACTIVE
    client.patch(f"/api/v1/review-cycles/{cycle_id_1}/status", headers=headers_a, json={"status": "ACTIVE"})
    
    # Create Review
    rev_res = client.post("/api/v1/reviews", headers=headers_a, json={
        "review_cycle_id": cycle_id_1,
        "employee_id": str(data["employee"].id),
        "title": "2026 Annual Review",
        "review_period_start": "2026-01-01",
        "review_period_end": "2026-12-31"
    })
    review_id_1 = rev_res.json()["id"]

def test_agent_failures_e2e(client, setup_test_data, db_session):
    data = setup_test_data
    token_manager_a = login(client, data["manager_a"].email, data["password"])
    headers_a = {"Authorization": f"Bearer {token_manager_a}"}
    
    from app.ai.agents.performance_analysis_agent import PerformanceAnalysisAgent
    from app.ai.agents.bias_detection_agent import BiasDetectionAgent
    
    original_perf = PerformanceAnalysisAgent._process
    original_bias = BiasDetectionAgent._process
    
    # --- TEST 1: Critical Agent Failure (Performance) ---
    cycle_res = client.post("/api/v1/review-cycles", headers=headers_a, json={
        "title": "2026 Annual Review",
        "start_date": "2026-01-01",
        "end_date": "2026-12-31"
    })
    cycle_id_1 = cycle_res.json()["id"]
    
    # Transition to ACTIVE
    client.patch(f"/api/v1/review-cycles/{cycle_id_1}/status", headers=headers_a, json={"status": "ACTIVE"})
    
    # Create Review
    rev_res = client.post("/api/v1/reviews", headers=headers_a, json={
        "review_cycle_id": cycle_id_1,
        "employee_id": str(data["employee"].id),
        "title": "2026 Annual Review",
        "review_period_start": "2026-01-01",
        "review_period_end": "2026-12-31"
    })
    review_id_1 = rev_res.json()["id"]
    
    client.post(f"/api/v1/reviews/{review_id_1}/inputs", headers=headers_a, json={
        "input_type": "SELF_ASSESSMENT",
        "content_text": "This is a detailed test input for performance failure. It has enough length."
    })
    
    def failing_perf_execute(*args, **kwargs):
        raise Exception("Mock LLM Performance Failure")
    
    original_perf = PerformanceAnalysisAgent._process
    PerformanceAnalysisAgent._process = failing_perf_execute
    try:
        trig_res = client.post(f"/api/v1/reviews/{review_id_1}/pipeline/trigger", headers=headers_a)
        if trig_res.status_code != 202: print('ERROR', trig_res.json()); assert trig_res.status_code == 202
        run_id_1 = trig_res.json()["pipeline_run_id"]
        
        # wait
        max_retries = 30
        completed = False
        for _ in range(max_retries):
            res = client.get(f"/api/v1/pipeline/{run_id_1}/status", headers=headers_a)
            if res.json()["pipeline_status"] == "FAILED":
                completed = True
                break
            time.sleep(1)
        assert completed, "Pipeline should fail"
    finally:
        PerformanceAnalysisAgent._process = original_perf
        
        cycle_check = client.get(f"/api/v1/reviews/{review_id_1}", headers=headers_a)
        assert cycle_check.json()["status"] == "PROCESSING", "Review remains processing on failed workflow"

    # --- TEST 2: Non-Critical Agent Failure (Bias) ---
    cycle_res = client.post("/api/v1/review-cycles", headers=headers_a, json={
        "title": "2026 Annual Review",
        "start_date": "2026-01-01",
        "end_date": "2026-12-31"
    })
    cycle_id_2 = cycle_res.json()["id"]
    client.patch(f"/api/v1/review-cycles/{cycle_id_2}/status", headers=headers_a, json={"status": "ACTIVE"})
    
    rev_res = client.post("/api/v1/reviews", headers=headers_a, json={
        "review_cycle_id": cycle_id_2,
        "employee_id": str(data["employee"].id),
        "title": "2026 Annual Review",
        "review_period_start": "2026-01-01",
        "review_period_end": "2026-12-31"
    })
    review_id_2 = rev_res.json()["id"]
    
    client.post(f"/api/v1/reviews/{review_id_2}/inputs", headers=headers_a, json={
        "input_type": "SELF_ASSESSMENT",
        "content_text": "This is another detailed test input for bias failure. It has enough length."
    })
    
    def failing_bias_execute(*args, **kwargs):
        raise Exception("Mock LLM Bias Failure")
    
    original_bias = BiasDetectionAgent._process
    BiasDetectionAgent._process = failing_bias_execute
    try:
        trig_res = client.post(f"/api/v1/reviews/{review_id_2}/pipeline/trigger", headers=headers_a)
        if trig_res.status_code != 202: print('ERROR', trig_res.json()); assert trig_res.status_code == 202
        run_id_2 = trig_res.json()["pipeline_run_id"]
        
        # wait
        completed = False
        for _ in range(max_retries):
            res = client.get(f"/api/v1/pipeline/{run_id_2}/status", headers=headers_a)
            st = res.json()["pipeline_status"]
            if st in ["COMPLETED", "FAILED"]:
                assert st == "COMPLETED", "Pipeline should complete despite bias failure (graceful degradation)"
                completed = True
                break
            time.sleep(1)
        assert completed, "Pipeline did not complete"
    finally:
        BiasDetectionAgent._process = original_bias
        
        cycle_check = client.get(f"/api/v1/reviews/{review_id_2}", headers=headers_a)
        assert cycle_check.json()["status"] == "PENDING_APPROVAL", "Review should proceed to pending approval"
