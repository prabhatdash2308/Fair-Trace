"""
FairTrace P2.0 — Tenant Isolation Tests

These tests verify that:
- Database queries are scoped by organization_id
- Cross-organization resource access is rejected at the authz layer
- The can() function acts as the final gate after DB scope

These tests are pure unit tests using the authz_service.can() function
and mock objects. They complement test_authz.py by focusing specifically
on multi-organization (multi-tenant) scenarios.

No database or HTTP connections are required.
"""
# ── Module-level stub: isolate from SQLAlchemy/DB dependencies ────────────────
import sys
import os
import types
import importlib.util

_BACKEND_PATH = os.path.join(os.path.dirname(__file__), "..")
if _BACKEND_PATH not in sys.path:
    sys.path.insert(0, _BACKEND_PATH)


def _ensure_model_stubs():
    """Stub models package so that models.enums can be imported without SQLAlchemy."""
    if 'models' not in sys.modules or not getattr(sys.modules.get('models'), '__stubbed__', False):
        models_pkg = types.ModuleType('models')
        models_pkg.__path__ = [os.path.join(_BACKEND_PATH, 'models')]
        models_pkg.__package__ = 'models'
        models_pkg.__stubbed__ = True
        sys.modules['models'] = models_pkg

        db_pkg = types.ModuleType('models.db')
        db_pkg.__path__ = [os.path.join(_BACKEND_PATH, 'models', 'db')]
        db_pkg.__package__ = 'models.db'
        sys.modules['models.db'] = db_pkg
        models_pkg.db = db_pkg

        user_mod = types.ModuleType('models.db.user')
        class _User: pass
        user_mod.User = _User
        sys.modules['models.db.user'] = user_mod
        db_pkg.user = user_mod

        spec = importlib.util.spec_from_file_location(
            'models.enums',
            os.path.join(_BACKEND_PATH, 'models', 'enums.py'),
        )
        enums_mod = importlib.util.module_from_spec(spec)
        sys.modules['models.enums'] = enums_mod
        spec.loader.exec_module(enums_mod)
        models_pkg.enums = enums_mod


_ensure_model_stubs()
# ─────────────────────────────────────────────────────────────────────────────

import uuid
from dataclasses import dataclass, field
from typing import Optional

import pytest

from models.enums import UserRole, ReviewStatus, ReportStatus, GoalStatus, FeedbackType
from services.authz_service import can, _resolve_organization_id



# ── Minimal mock objects ───────────────────────────────────────────────────────

@dataclass
class User:
    id: uuid.UUID
    role: UserRole
    organization_id: Optional[uuid.UUID]
    email: str = "user@test.com"
    full_name: str = "Test User"
    manager_id: Optional[uuid.UUID] = None


@dataclass
class Review:
    id: uuid.UUID
    organization_id: uuid.UUID
    employee_id: uuid.UUID
    manager_id: uuid.UUID
    status: ReviewStatus = ReviewStatus.DRAFT


@dataclass
class Report:
    id: uuid.UUID
    status: ReportStatus
    review: Review

    @property
    def organization_id(self):
        return None  # resolved via review


@dataclass
class Goal:
    id: uuid.UUID
    organization_id: uuid.UUID
    employee_id: uuid.UUID
    employee: Optional[object] = None


@dataclass
class Feedback:
    id: uuid.UUID
    organization_id: uuid.UUID
    author_id: uuid.UUID
    recipient_id: uuid.UUID
    recipient: Optional[object] = None


@dataclass
class Employee:
    id: uuid.UUID
    organization_id: uuid.UUID
    manager_id: Optional[uuid.UUID] = None


# ── Constants ──────────────────────────────────────────────────────────────────

ORG_A = uuid.UUID("a0000000-0000-0000-0000-000000000000")
ORG_B = uuid.UUID("b0000000-0000-0000-0000-000000000000")

# Org A actors
A_ADMIN   = User(id=uuid.UUID("a0000000-0000-0000-0000-000000000001"), role=UserRole.ORG_ADMIN,   organization_id=ORG_A)
A_MANAGER = User(id=uuid.UUID("a0000000-0000-0000-0000-000000000002"), role=UserRole.MANAGER,     organization_id=ORG_A)
A_EMP     = User(id=uuid.UUID("a0000000-0000-0000-0000-000000000003"), role=UserRole.EMPLOYEE,    organization_id=ORG_A)

# Org B actors
B_ADMIN   = User(id=uuid.UUID("b0000000-0000-0000-0000-000000000001"), role=UserRole.ORG_ADMIN,   organization_id=ORG_B)
B_MANAGER = User(id=uuid.UUID("b0000000-0000-0000-0000-000000000002"), role=UserRole.MANAGER,     organization_id=ORG_B)
B_EMP     = User(id=uuid.UUID("b0000000-0000-0000-0000-000000000003"), role=UserRole.EMPLOYEE,    organization_id=ORG_B)

# Resources in Org A
A_EMP_RECORD = Employee(id=A_EMP.id,     organization_id=ORG_A, manager_id=A_MANAGER.id)
A_EMP2_REC   = Employee(id=uuid.UUID("a0000000-0000-0000-0000-000000000004"), organization_id=ORG_A)

# Resources in Org B
B_EMP_RECORD = Employee(id=B_EMP.id, organization_id=ORG_B, manager_id=B_MANAGER.id)

A_REVIEW = Review(id=uuid.uuid4(), organization_id=ORG_A, employee_id=A_EMP.id, manager_id=A_MANAGER.id)
B_REVIEW = Review(id=uuid.uuid4(), organization_id=ORG_B, employee_id=B_EMP.id, manager_id=B_MANAGER.id)

A_REPORT_FINAL = Report(id=uuid.uuid4(), status=ReportStatus.FINALIZED, review=A_REVIEW)
A_REPORT_DRAFT = Report(id=uuid.uuid4(), status=ReportStatus.DRAFT,     review=A_REVIEW)
B_REPORT_FINAL = Report(id=uuid.uuid4(), status=ReportStatus.FINALIZED, review=B_REVIEW)

A_GOAL = Goal(id=uuid.uuid4(), organization_id=ORG_A, employee_id=A_EMP.id, employee=A_EMP_RECORD)
B_GOAL = Goal(id=uuid.uuid4(), organization_id=ORG_B, employee_id=B_EMP.id, employee=B_EMP_RECORD)

A_FEEDBACK = Feedback(
    id=uuid.uuid4(), organization_id=ORG_A,
    author_id=A_MANAGER.id, recipient_id=A_EMP.id,
    recipient=A_EMP_RECORD,
)
B_FEEDBACK = Feedback(
    id=uuid.uuid4(), organization_id=ORG_B,
    author_id=B_MANAGER.id, recipient_id=B_EMP.id,
    recipient=B_EMP_RECORD,
)

A_PENDING_REVIEW = Review(
    id=uuid.uuid4(), organization_id=ORG_A,
    employee_id=A_EMP.id, manager_id=A_MANAGER.id,
    status=ReviewStatus.PENDING_APPROVAL,
)


# ── resolve_organization_id helper tests ──────────────────────────────────────

class TestResolveOrganizationId:
    """Verify the org-id resolver works for all resource types."""

    def test_resolves_direct_org_id(self):
        assert _resolve_organization_id(A_REVIEW) == str(ORG_A)
        assert _resolve_organization_id(B_REVIEW) == str(ORG_B)

    def test_resolves_goal_org_id(self):
        assert _resolve_organization_id(A_GOAL) == str(ORG_A)

    def test_resolves_feedback_org_id(self):
        assert _resolve_organization_id(A_FEEDBACK) == str(ORG_A)

    def test_resolves_report_via_review(self):
        # Report has no org_id directly; resolved via .review
        assert _resolve_organization_id(A_REPORT_FINAL) == str(ORG_A)
        assert _resolve_organization_id(B_REPORT_FINAL) == str(ORG_B)

    def test_resolves_employee_org_id(self):
        assert _resolve_organization_id(A_EMP_RECORD) == str(ORG_A)

    def test_returns_none_for_none(self):
        assert _resolve_organization_id(None) is None


# ── Test: Org A cannot access Org B employees ─────────────────────────────────

class TestCrossTenantEmployeeIsolation:
    """Test 6: Organization A cannot access Organization B employees."""

    def test_a_admin_blocked_from_b_employee(self):
        assert can(A_ADMIN,   "people.read", B_EMP_RECORD) is False

    def test_a_manager_blocked_from_b_employee(self):
        assert can(A_MANAGER, "people.read", B_EMP_RECORD) is False

    def test_a_employee_blocked_from_b_employee(self):
        assert can(A_EMP,     "people.read", B_EMP_RECORD) is False

    def test_b_admin_blocked_from_a_employee(self):
        assert can(B_ADMIN,   "people.read", A_EMP_RECORD) is False

    def test_a_admin_can_read_a_employee(self):
        """Positive control: Org A admin can read Org A employee."""
        assert can(A_ADMIN, "people.read", A_EMP_RECORD) is True

    def test_b_admin_can_read_b_employee(self):
        """Positive control: Org B admin can read Org B employee."""
        assert can(B_ADMIN, "people.read", B_EMP_RECORD) is True


# ── Test: Org A cannot access Org B reviews ───────────────────────────────────

class TestCrossTenantReviewIsolation:
    """Test 7: Organization A cannot access Organization B reviews."""

    def test_a_admin_blocked_from_b_review(self):
        assert can(A_ADMIN,   "review.read", B_REVIEW) is False

    def test_a_manager_blocked_from_b_review(self):
        assert can(A_MANAGER, "review.read", B_REVIEW) is False

    def test_a_employee_blocked_from_b_review(self):
        assert can(A_EMP,     "review.read", B_REVIEW) is False

    def test_a_manager_cannot_approve_b_review(self):
        b_pending = Review(
            id=uuid.uuid4(), organization_id=ORG_B,
            employee_id=B_EMP.id, manager_id=B_MANAGER.id,
            status=ReviewStatus.PENDING_APPROVAL,
        )
        assert can(A_MANAGER, "review.approve", b_pending) is False

    def test_a_admin_can_read_a_review(self):
        """Positive control."""
        assert can(A_ADMIN, "review.read", A_REVIEW) is True

    def test_b_admin_can_read_b_review(self):
        """Positive control."""
        assert can(B_ADMIN, "review.read", B_REVIEW) is True


# ── Test: Org A cannot access Org B goals ─────────────────────────────────────

class TestCrossTenantGoalIsolation:
    """Test 8: Organization A cannot access Organization B goals."""

    def test_a_admin_blocked_from_b_goal(self):
        assert can(A_ADMIN,   "goal.read", B_GOAL) is False

    def test_a_manager_blocked_from_b_goal(self):
        assert can(A_MANAGER, "goal.read", B_GOAL) is False

    def test_a_employee_blocked_from_b_goal(self):
        assert can(A_EMP,     "goal.read", B_GOAL) is False

    def test_a_employee_can_read_own_a_goal(self):
        """Positive control."""
        assert can(A_EMP, "goal.read", A_GOAL) is True

    def test_b_admin_blocked_from_a_goal(self):
        assert can(B_ADMIN, "goal.read", A_GOAL) is False


# ── Test: Org A cannot access Org B feedback ──────────────────────────────────

class TestCrossTenantFeedbackIsolation:
    """Test 9: Organization A cannot access Organization B feedback."""

    def test_a_admin_blocked_from_b_feedback(self):
        assert can(A_ADMIN,   "feedback.read", B_FEEDBACK) is False

    def test_a_manager_blocked_from_b_feedback(self):
        assert can(A_MANAGER, "feedback.read", B_FEEDBACK) is False

    def test_a_employee_blocked_from_b_feedback(self):
        assert can(A_EMP,     "feedback.read", B_FEEDBACK) is False

    def test_b_admin_blocked_from_a_feedback(self):
        assert can(B_ADMIN, "feedback.read", A_FEEDBACK) is False

    def test_a_manager_can_read_a_feedback(self):
        """Positive control: Org A manager can read Org A feedback they authored."""
        assert can(A_MANAGER, "feedback.read", A_FEEDBACK) is True


# ── Test: Cross-tenant report isolation ───────────────────────────────────────

class TestCrossTenantReportIsolation:
    """Cross-org reports must be blocked (for export too)."""

    def test_a_manager_blocked_from_b_report(self):
        assert can(A_MANAGER, "report.read", B_REPORT_FINAL) is False

    def test_a_employee_blocked_from_b_report(self):
        assert can(A_EMP,     "report.read", B_REPORT_FINAL) is False

    def test_a_admin_blocked_from_b_report(self):
        assert can(A_ADMIN,   "report.read", B_REPORT_FINAL) is False

    def test_a_manager_blocked_from_b_export(self):
        assert can(A_MANAGER, "export.read", B_REPORT_FINAL) is False

    def test_a_admin_blocked_from_b_export(self):
        assert can(A_ADMIN, "export.read", B_REPORT_FINAL) is False

    def test_a_manager_can_read_a_report(self):
        """Positive control."""
        assert can(A_MANAGER, "report.read", A_REPORT_FINAL) is True

    def test_a_employee_can_read_own_finalized_a_report(self):
        """Positive control."""
        assert can(A_EMP, "report.read", A_REPORT_FINAL) is True


# ── Test: Approval and transition isolation ───────────────────────────────────

class TestReviewTransitionIsolation:
    """Tests 10-11: Transition rules and employee-cannot-approve."""

    def test_employee_cannot_approve_any_review(self):
        assert can(A_EMP, "review.approve", A_PENDING_REVIEW) is False

    def test_b_employee_cannot_approve_b_review(self):
        b_pending = Review(
            id=uuid.uuid4(), organization_id=ORG_B,
            employee_id=B_EMP.id, manager_id=B_MANAGER.id,
            status=ReviewStatus.PENDING_APPROVAL,
        )
        assert can(B_EMP, "review.approve", b_pending) is False

    def test_correct_manager_can_approve(self):
        assert can(A_MANAGER, "review.approve", A_PENDING_REVIEW) is True

    def test_wrong_org_manager_cannot_approve(self):
        assert can(B_MANAGER, "review.approve", A_PENDING_REVIEW) is False

    def test_employee_can_acknowledge_own(self):
        approved_review = Review(
            id=uuid.uuid4(), organization_id=ORG_A,
            employee_id=A_EMP.id, manager_id=A_MANAGER.id,
            status=ReviewStatus.APPROVED,
        )
        assert can(A_EMP, "review.acknowledge", approved_review) is True

    def test_manager_cannot_acknowledge(self):
        approved_review = Review(
            id=uuid.uuid4(), organization_id=ORG_A,
            employee_id=A_EMP.id, manager_id=A_MANAGER.id,
            status=ReviewStatus.APPROVED,
        )
        assert can(A_MANAGER, "review.acknowledge", approved_review) is False

    def test_cross_tenant_acknowledge_blocked(self):
        approved_a = Review(
            id=uuid.uuid4(), organization_id=ORG_A,
            employee_id=A_EMP.id, manager_id=A_MANAGER.id,
            status=ReviewStatus.APPROVED,
        )
        assert can(B_EMP, "review.acknowledge", approved_a) is False


# ── Regression: ensure tenant_isolation is enforced BEFORE role checks ─────────

class TestTenantIsolationPrecondition:
    """Tenant isolation must be the first gate — even admin roles fail cross-tenant."""

    def test_super_admin_blocked_cross_tenant(self):
        super_admin_a = User(
            id=uuid.uuid4(), role=UserRole.SUPER_ADMIN,
            organization_id=ORG_A,
        )
        assert can(super_admin_a, "review.read", B_REVIEW) is False

    def test_hr_admin_blocked_cross_tenant(self):
        hr_admin_a = User(
            id=uuid.uuid4(), role=UserRole.HR_ADMIN,
            organization_id=ORG_A,
        )
        assert can(hr_admin_a, "goal.read", B_GOAL) is False

    def test_org_admin_blocked_cross_tenant_feedback(self):
        assert can(A_ADMIN, "feedback.read", B_FEEDBACK) is False
