import sys
import os
import uuid
from datetime import datetime, timedelta
import random

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.database import SessionLocal, engine
from models.db.base import Base
from models.db.user import User
from models.db.review_cycle import ReviewCycle
from models.db.review_input import ReviewInput
from models.db.document import Document
from models.db.document_chunk import DocumentChunk
from models.db.report import Report
from models.db.audit_event import AuditEvent
from models.db.bias_flag import BiasFlag
from models.db.performance_claim import PerformanceClaim
from models.db.evidence_citation import EvidenceCitation
from models.db.export import ReportExport
from models.db.workflow import WorkflowExecution, ApprovalRequest, WorkflowHistory
from models.db.agent_execution import AgentExecution
from models.db.organization import Organization
from core.security import hash_password
from models.enums import (
    UserRole, ReviewCycleStatus, InputType, DocumentStatus, ReportStatus, 
    PerformanceDimension, ConfidenceLevel, BiasType, Severity, AuditEventType
)

def seed_db():
    seed_password = os.environ.get("FAIRTRACE_SEED_PASSWORD")
    if not seed_password:
        print("ERROR: FAIRTRACE_SEED_PASSWORD is required.")
        sys.exit(1)

    print("Starting database seeding...")
    db = SessionLocal()
    
    try:
        # Create tables if they do not exist
        Base.metadata.create_all(bind=engine)

        # Clear existing data in reverse dependency order
        print("Clearing old data...")
        db.query(AgentExecution).delete()
        db.query(WorkflowHistory).delete()
        db.query(ApprovalRequest).delete()
        db.query(ReportExport).delete()
        db.query(WorkflowExecution).delete()
        db.query(BiasFlag).delete()
        db.query(EvidenceCitation).delete()
        db.query(PerformanceClaim).delete()
        db.query(Report).delete()
        db.query(DocumentChunk).delete()
        db.query(Document).delete()
        db.query(ReviewInput).delete()
        db.query(ReviewCycle).delete()
        db.query(AuditEvent).delete()
        db.query(ReviewCycle).delete()
        db.query(User).delete()
        db.query(Organization).delete()
        db.commit()
        print("Old data cleared.")

        # Seed Organization
        org = Organization(id=uuid.uuid4(), name="FairTrace Demo Corp")
        db.add(org)
        db.commit()

        # 1 Admin
        admin = User(
            email="admin@fairtrace.ai",
            password_hash=hash_password(seed_password),
            full_name="Admin User",
            role=UserRole.ADMIN,
            organization_id=org.id,
            is_active=True
        )
        db.add(admin)
        db.commit()

        # 2 Managers
        managers = []
        for i in range(1, 3):
            manager = User(
                email=f"manager{i}@fairtrace.ai",
                password_hash=hash_password(seed_password),
                full_name=f"Manager {i}",
                role=UserRole.MANAGER,
                organization_id=org.id,
                is_active=True
            )
            db.add(manager)
            managers.append(manager)
        db.commit()

        # 15 Employees
        employees = []
        for i in range(1, 16):
            manager = managers[i % 2]
            employee = User(
                email=f"employee{i}@fairtrace.ai",
                password_hash=hash_password(seed_password),
                full_name=f"Employee {i}",
                role=UserRole.EMPLOYEE,
                manager_id=manager.id,
                organization_id=org.id,
                is_active=True
            )
            db.add(employee)
            employees.append(employee)
        db.commit()

        print(f"Created Admin, {len(managers)} Managers, {len(employees)} Employees.")

        # Review Cycles, Inputs, Documents, Reports, etc.
        cycle_statuses = [ReviewCycleStatus.COMPLETED, ReviewCycleStatus.ACTIVE, ReviewCycleStatus.PROCESSING, ReviewCycleStatus.DRAFT, ReviewCycleStatus.PENDING_APPROVAL]
        
        for i, employee in enumerate(employees):
            status = cycle_statuses[i % len(cycle_statuses)]
            
            cycle = ReviewCycle(
                employee_id=employee.id,
                manager_id=employee.manager_id,
                created_by=admin.id,
                organization_id=org.id,
                title=f"2026 Annual Review - {employee.full_name}",
                review_period_start=datetime.utcnow() - timedelta(days=365),
                review_period_end=datetime.utcnow(),
                status=status
            )
            db.add(cycle)
            db.commit()

            # Audit Event for Cycle Creation
            audit_event = AuditEvent(
                event_type=AuditEventType.REVIEW_CYCLE_CREATED,
                actor_id=admin.id,
                actor_role=admin.role,
                resource_type="ReviewCycle",
                resource_id=cycle.id,
                event_payload={"title": cycle.title}
            )
            db.add(audit_event)

            if status != ReviewCycleStatus.DRAFT:
                # Document
                doc = Document(
                    owner_id=employee.id,
                    original_filename=f"achievements_{employee.id}.pdf",
                    mime_type="application/pdf",
                    extension=".pdf",
                    file_size_bytes=random.randint(100000, 500000),
                    storage_key=f"uploads/{employee.id}/{uuid.uuid4()}.pdf",
                    checksum=str(uuid.uuid4()),
                    status=DocumentStatus.STORED,
                    page_count=5,
                    character_count=15000
                )
                db.add(doc)
                db.commit()

                # Review Input
                rev_input = ReviewInput(
                    review_cycle_id=cycle.id,
                    submitted_by=employee.id,
                    input_type=InputType.SELF_ASSESSMENT,
                    content_text="Delivered multiple high-impact features successfully.",
                    is_anonymized=False
                )
                db.add(rev_input)
                db.commit()
                
                if status in [ReviewCycleStatus.COMPLETED, ReviewCycleStatus.PENDING_APPROVAL]:
                    report_status = ReportStatus.FINALIZED if status == ReviewCycleStatus.COMPLETED else ReportStatus.PENDING_APPROVAL
                    
                    report = Report(
                        review_cycle_id=cycle.id,
                        status=report_status,
                        executive_summary="Excellent performance overall with great technical execution.",
                        recommended_actions=["Promote to next level", "Assign lead role on new project"],
                        confidence_score=ConfidenceLevel.HIGH,
                        pipeline_run_id=f"run_{uuid.uuid4()}",
                        approved_by=cycle.manager_id if status == ReviewCycleStatus.COMPLETED else None,
                        approved_at=datetime.utcnow() if status == ReviewCycleStatus.COMPLETED else None
                    )
                    db.add(report)
                    db.commit()

                    # Performance Claim
                    claim = PerformanceClaim(
                        report_id=report.id,
                        dimension=PerformanceDimension.TECHNICAL,
                        claim_text="Demonstrated strong technical leadership.",
                        explanation="Consistent delivery of complex architectures.",
                        confidence=ConfidenceLevel.HIGH,
                        is_supported=True,
                        display_order=1
                    )
                    db.add(claim)
                    db.commit()

                    # Evidence Citation
                    citation = EvidenceCitation(
                        claim_id=claim.id,
                        review_input_id=rev_input.id,
                        extracted_passage="I led the backend rewrite project.",
                        similarity_score=0.92,
                        retrieval_rank=1
                    )
                    db.add(citation)
                    
                    # Bias Flag
                    if random.random() > 0.7:
                        bias = BiasFlag(
                            report_id=report.id,
                            review_input_id=rev_input.id,
                            bias_type=BiasType.RECENCY,
                            severity=Severity.MEDIUM,
                            affected_text="Has been doing great lately.",
                            recommended_action="Consider evaluating the entire year.",
                            detected_by_agent="bias_detector_v1",
                            detection_reasoning="Focus is solely on the last 2 months."
                        )
                        db.add(bias)

                    db.commit()

        print("Database successfully seeded!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
