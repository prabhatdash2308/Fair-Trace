import sys
import os
import uuid
from datetime import datetime, timedelta
import random

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.database import SessionLocal, engine
from models.db.base import Base
from models.db.user import User
from models.db.review_cycle import ReviewCycle
from models.db.review_input import ReviewInput
from models.db.document import Document
from models.db.report import Report
from core.security import hash_password
from models.enums import UserRole, ReviewCycleStatus, InputType, DocumentStatus, ReportStatus

from models.db.audit_event import AuditEvent

def seed_db():
    print("Starting database seeding...")
    db = SessionLocal()
    
    try:
        # Create tables if not exist
        Base.metadata.create_all(bind=engine)

        # Clear existing data
        db.query(AuditEvent).delete()
        db.query(Report).delete()
        db.query(Document).delete()
        db.query(ReviewInput).delete()
        db.query(ReviewCycle).delete()
        db.query(User).delete()
        db.commit()

        # 1 Admin
        admin = User(
            email="admin@reviewguard.ai",
            password_hash=hash_password("admin123"),
            full_name="Admin User",
            role=UserRole.ADMIN,
            is_active=True
        )
        db.add(admin)
        db.commit()

        # 2 Managers
        managers = []
        for i in range(2):
            manager = User(
                email=f"manager{i+1}@reviewguard.ai",
                password_hash=hash_password("manager123"),
                full_name=f"Manager {i+1}",
                role=UserRole.MANAGER,
                is_active=True
            )
            db.add(manager)
            managers.append(manager)
        db.commit()

        # 15 Employees
        employees = []
        for i in range(15):
            manager = managers[i % 2]
            employee = User(
                email=f"employee{i+1}@reviewguard.ai",
                password_hash=hash_password("employee123"),
                full_name=f"Employee {i+1}",
                role=UserRole.EMPLOYEE,
                manager_id=manager.id,
                is_active=True
            )
            db.add(employee)
            employees.append(employee)
        db.commit()

        # 5 Review Cycles
        cycles = []
        statuses = [ReviewCycleStatus.COMPLETED, ReviewCycleStatus.ACTIVE, ReviewCycleStatus.COMPLETED, ReviewCycleStatus.PROCESSING, ReviewCycleStatus.DRAFT]
        for i in range(5):
            employee = random.choice(employees)
            cycle = ReviewCycle(
                employee_id=employee.id,
                manager_id=employee.manager_id,
                created_by=admin.id,
                title=f"Q{i%4 + 1} 2026 Performance Review - {employee.full_name}",
                review_period_start=datetime.utcnow() - timedelta(days=90),
                review_period_end=datetime.utcnow(),
                status=statuses[i]
            )
            db.add(cycle)
            cycles.append(cycle)
        db.commit()

        # Review Inputs and Documents
        reports_created = 0
        for cycle in cycles:
            if cycle.status == ReviewCycleStatus.COMPLETED:
                doc = Document(
                    owner_id=cycle.employee_id,
                    original_filename=f"self_assessment_{cycle.id}.pdf",
                    mime_type="application/pdf",
                    extension=".pdf",
                    file_size_bytes=random.randint(100000, 500000),
                    storage_key=f"uploads/{cycle.employee_id}/{uuid.uuid4()}.pdf",
                    checksum=str(uuid.uuid4()),
                    status=DocumentStatus.STORED,
                    page_count=3,
                    character_count=5000
                )
                db.add(doc)
                db.commit()

                rev_input = ReviewInput(
                    review_cycle_id=cycle.id,
                    input_type=InputType.SELF_ASSESSMENT,
                    content_text="Great year, lots of deliverables.",
                    submitted_by=cycle.employee_id
                )
                db.add(rev_input)
                
                # Reports
                if reports_created < 20:
                    report = Report(
                        review_cycle_id=cycle.id,
                        status=ReportStatus.FINALIZED,
                        executive_summary="The employee demonstrated excellent performance.",
                        recommended_actions=["Promote to Senior", "Give a raise"],
                        pipeline_run_id=f"run_{uuid.uuid4()}",
                        approved_by=cycle.manager_id,
                        approved_at=datetime.utcnow()
                    )
                    db.add(report)
                    reports_created += 1

        db.commit()
        print(f"Database successfully seeded: 1 Admin, {len(managers)} Managers, {len(employees)} Employees, {len(cycles)} Cycles, and associated Reports.")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
