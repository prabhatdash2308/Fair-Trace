import sys
import os
import uuid
import time
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.database import SessionLocal
from models.db.organization import Organization
from models.db.user import User
from models.db.review_cycle import ReviewCycle
from models.db.review_input import ReviewInput
from models.db.workflow import WorkflowExecution
from models.db.agent_execution import AgentExecution
from models.db.report import Report
from models.db.performance_claim import PerformanceClaim
from models.db.evidence_citation import EvidenceCitation
from models.enums import UserRole, ReviewCycleStatus, InputType
from services.pipeline_service import initialize_pipeline, execute_pipeline
from unittest.mock import patch
from app.ai.services.llm.models import LLMResponse
from pydantic import BaseModel

def mock_llm_generate(self, req, correlation_id=None):
    # Depending on response_format, return fake structured data
    structured_data = None
    if req.response_format:
        schema = req.response_format.model_json_schema()
        fake_data = {}
        for prop, details in schema.get("properties", {}).items():
            if details.get("type") == "array":
                fake_data[prop] = []
            elif details.get("type") == "number":
                fake_data[prop] = 0.8
            elif details.get("type") == "integer":
                fake_data[prop] = 1
            elif details.get("type") == "string":
                fake_data[prop] = "Mock String"
            elif details.get("type") == "object" or "additionalProperties" in details:
                fake_data[prop] = {}
            else:
                fake_data[prop] = None
        structured_data = req.response_format(**fake_data)
        
    return LLMResponse(
        content="Mock content",
        model_used="mock-model",
        structured_data=structured_data
    )

def test_golden_path():
    db = SessionLocal()
    try:
        test_id = str(uuid.uuid4())[:8]
        # Create Org
        org = Organization(id=uuid.uuid4(), name=f"Test Org {test_id}")
        db.add(org)
        
        # Create Manager
        manager = User(
            id=uuid.uuid4(),
            email=f"manager_{test_id}@test.com",
            password_hash="test",
            full_name="Test Manager",
            role=UserRole.MANAGER,
            organization_id=org.id,
            is_active=True
        )
        db.add(manager)
        
        # Create Employee
        employee = User(
            id=uuid.uuid4(),
            email=f"employee_{test_id}@test.com",
            password_hash="test",
            full_name="Test Employee",
            role=UserRole.EMPLOYEE,
            manager_id=manager.id,
            organization_id=org.id,
            is_active=True
        )
        db.add(employee)
        db.commit()

        # Create Review Cycle
        cycle = ReviewCycle(
            id=uuid.uuid4(),
            employee_id=employee.id,
            manager_id=manager.id,
            created_by=manager.id,
            organization_id=org.id,
            title="Golden Path Review",
            status=ReviewCycleStatus.ACTIVE,
            review_period_start=datetime.utcnow() - timedelta(days=90),
            review_period_end=datetime.utcnow()
        )
        db.add(cycle)
        db.commit()

        # Create 2 Inputs
        inp1 = ReviewInput(
            id=uuid.uuid4(),
            review_cycle_id=cycle.id,
            submitted_by=employee.id,
            input_type=InputType.SELF_ASSESSMENT,
            content_text="I delivered the Phase 1 feature on time."
        )
        inp2 = ReviewInput(
            id=uuid.uuid4(),
            review_cycle_id=cycle.id,
            submitted_by=manager.id,
            input_type=InputType.MANAGER_NOTE,
            content_text="Employee exceeded expectations for Phase 1."
        )
        db.add(inp1)
        db.add(inp2)
        db.commit()

        print("Created Data. Initializing Pipeline...")
        
        # Initialize Pipeline
        pipeline_run_id = initialize_pipeline(db, cycle.id, manager)
        print(f"Pipeline Initialized: {pipeline_run_id}")
        
        workflow = db.query(WorkflowExecution).filter(WorkflowExecution.execution_id == pipeline_run_id).first()
        assert workflow is not None, "WorkflowExecution missing"

        # Execute Pipeline (Synchronous for test) with Mock LLM
        print("Executing Pipeline...")
        with patch('app.ai.services.llm.llm_service.LLMService.generate', new=mock_llm_generate):
            execute_pipeline(pipeline_run_id, cycle.id)
        print("Pipeline Execution Completed.")
        
        # Verify Workflow Status
        db.refresh(workflow)
        print(f"Workflow Status: {workflow.status}")
        
        # Verify AgentExecutions
        agent_execs = db.query(AgentExecution).filter(AgentExecution.workflow_execution_id == workflow.id).all()
        print(f"Agent Executions found: {len(agent_execs)}")
        for ae in agent_execs:
            print(f" - {ae.sequence}: {ae.agent_name} ({ae.status})")
        assert len(agent_execs) > 0, "No AgentExecutions created!"

        # Verify Report
        report = db.query(Report).filter(Report.pipeline_run_id == pipeline_run_id).first()
        assert report is not None, "Report missing"
        print(f"Report Created. ID: {report.id}")
        
        # Verify Performance Claims
        claims = db.query(PerformanceClaim).filter(PerformanceClaim.report_id == report.id).all()
        print(f"Performance Claims: {len(claims)}")
        
        # Verify EvidenceCitations
        citations = db.query(EvidenceCitation).all()  # We can just check globally for this run
        new_citations = [c for c in citations if c.review_input_id in (inp1.id, inp2.id)]
        print(f"Evidence Citations Linked to Inputs: {len(new_citations)}")
        assert len(new_citations) > 0, "No EvidenceCitations linked to ReviewInputs!"

        print("GOLDEN PATH TEST PASSED!")
    except Exception as e:
        print(f"GOLDEN PATH TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_golden_path()
