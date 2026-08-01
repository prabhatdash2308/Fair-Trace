"""
ReviewGuard AI — Database Seed Script
Creates initial admin user and demo data for hackathon demo.
Run once after migrations: python seed.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import date
from core.database import SessionLocal
from core.security import hash_password
from models.db.user import User
from models.db.review_cycle import ReviewCycle
from models.db.review_input import ReviewInput
from models.enums import UserRole, ReviewCycleStatus, InputType

def seed():
    db = SessionLocal()
    try:
        # Check if already seeded
        if db.query(User).count() > 0:
            print("Database already seeded. Skipping.")
            return

        print("Seeding database...")

        # Admin User
        admin = User(
            email="admin@reviewguard.ai",
            password_hash=hash_password("admin123456"),
            full_name="System Admin",
            role=UserRole.ADMIN,
            is_active=True,
        )
        db.add(admin)
        db.flush()

        # Manager
        manager = User(
            email="manager@reviewguard.ai",
            password_hash=hash_password("manager123456"),
            full_name="Alex Chen",
            role=UserRole.MANAGER,
            is_active=True,
        )
        db.add(manager)
        db.flush()

        # Employee (reports to manager)
        employee = User(
            email="employee@reviewguard.ai",
            password_hash=hash_password("employee123456"),
            full_name="Jordan Smith",
            role=UserRole.EMPLOYEE,
            manager_id=manager.id,
            is_active=True,
        )
        db.add(employee)
        db.flush()

        # Review Cycle (ACTIVE — ready for pipeline demo)
        cycle = ReviewCycle(
            employee_id=employee.id,
            manager_id=manager.id,
            created_by=manager.id,
            title="Q3 2026 Performance Review",
            review_period_start=date(2026, 4, 1),
            review_period_end=date(2026, 6, 30),
            status=ReviewCycleStatus.ACTIVE,
        )
        db.add(cycle)
        db.flush()

        # Review Inputs
        inputs = [
            ReviewInput(
                review_cycle_id=cycle.id,
                submitted_by=employee.id,
                input_type=InputType.SELF_ASSESSMENT,
                content_text=(
                    "This quarter I led the migration of our authentication service to OAuth 2.0, "
                    "which reduced login latency by 40%. I collaborated extensively with the frontend team "
                    "to design the new token refresh flow and mentored two junior engineers through "
                    "their first production deployments. I also proactively identified and resolved "
                    "a critical race condition in our payment processing pipeline before it reached production. "
                    "My primary growth area is public speaking and presenting technical concepts to non-technical stakeholders. "
                    "I am actively working on this through bi-weekly presentations to the product team."
                ),
                is_anonymized=False,
            ),
            ReviewInput(
                review_cycle_id=cycle.id,
                submitted_by=manager.id,
                input_type=InputType.MANAGER_NOTE,
                content_text=(
                    "Jordan consistently delivers high-quality code with exceptional attention to technical detail. "
                    "The OAuth migration was completed two weeks ahead of schedule with zero production incidents. "
                    "Jordan's mentoring contributions have measurably improved the team's code review quality. "
                    "The proactive identification of the payment pipeline race condition saved an estimated "
                    "$50K in potential incident response costs. "
                    "Key growth opportunity: Jordan should develop stronger skills in cross-functional communication "
                    "and stakeholder management to move toward a senior role."
                ),
                is_anonymized=False,
            ),
            ReviewInput(
                review_cycle_id=cycle.id,
                submitted_by=admin.id,   # peer
                input_type=InputType.PEER_REVIEW,
                content_text=(
                    "Jordan is one of the most reliable engineers I have worked with. "
                    "During the auth migration project, Jordan was always available for design discussions "
                    "and provided thorough, constructive code reviews. "
                    "Jordan's debugging skills are exceptional — on two occasions Jordan resolved issues "
                    "that had blocked the rest of the team for days. "
                    "My one suggestion: Jordan could communicate status updates more proactively "
                    "so the team is aware of blockers earlier."
                ),
                is_anonymized=True,
            ),
            ReviewInput(
                review_cycle_id=cycle.id,
                submitted_by=manager.id,
                input_type=InputType.PROJECT_OUTCOME,
                content_text=(
                    "Project: OAuth 2.0 Authentication Migration\n"
                    "Outcome: Successfully completed Q3 deliverable. "
                    "40% reduction in login latency. Zero production incidents during rollout. "
                    "Delivered 2 weeks ahead of schedule.\n\n"
                    "Project: Payment Pipeline Reliability\n"
                    "Outcome: Jordan identified and resolved a critical race condition during code review. "
                    "The fix was merged and deployed with full test coverage. "
                    "Estimated business impact: $50K avoided incident cost."
                ),
                is_anonymized=False,
            ),
        ]
        for inp in inputs:
            db.add(inp)

        db.commit()
        print("✅ Seed complete!")
        print("─" * 40)
        print(f"  Admin:    admin@reviewguard.ai     / admin123456")
        print(f"  Manager:  manager@reviewguard.ai   / manager123456")
        print(f"  Employee: employee@reviewguard.ai  / employee123456")
        print(f"  Review Cycle ID: {cycle.id}")
        print("─" * 40)
        print("  Next step: POST /api/v1/review-cycles/{id}/pipeline/trigger")

    except Exception as exc:
        db.rollback()
        print(f"❌ Seed failed: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
