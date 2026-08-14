"""FairTrace — Authorization Service (P2.0)

Centralized RBAC and tenant isolation decisions.
All policy functions accept CurrentUser (the authenticated context),
NOT the User ORM object — the User ORM is only needed for relationship checks
which require a DB query, and those are explicitly noted.

can(user, action, resource=None) -> bool
    Returns True iff the user is permitted to perform the action on the resource.
    Tenant isolation is enforced as a hard boundary: if the resource belongs to
    a different organization than the user, access is denied regardless of role.

Defense-in-depth: callers must ALSO scope DB queries by organization_id.
The can() check here is the final gate after the query.
"""

from __future__ import annotations

import logging
from typing import Any, TYPE_CHECKING

from models.enums import UserRole

if TYPE_CHECKING:
    from dependencies import CurrentUser

logger = logging.getLogger(__name__)

# Roles that have broad admin access within their organization
_ADMIN_ROLES = frozenset({
    UserRole.ORG_ADMIN,
    UserRole.SUPER_ADMIN,
    UserRole.HR_ADMIN,
})


class AuthorizationError(Exception):
    """Raised internally when a policy violation is detected."""


# ── Helpers ────────────────────────────────────────────────────────────────────

def _resolve_organization_id(resource: Any) -> str | None:
    """Safely extract organization_id from a resource or its parents."""
    if not resource:
        return None
    if hasattr(resource, "organization_id") and resource.organization_id is not None:
        return str(resource.organization_id)
    # Report → Review → organization_id
    if hasattr(resource, "review") and resource.review is not None:
        if hasattr(resource.review, "organization_id") and resource.review.organization_id is not None:
            return str(resource.review.organization_id)
    # ReviewInput → Review → organization_id (via review_id, not always loaded)
    return None


def _is_admin(user: "CurrentUser") -> bool:
    """Return True if the user holds any admin-level role."""
    return user.role in _ADMIN_ROLES


def _is_manager_of(user: "CurrentUser", employee_id: Any) -> bool:
    """
    Check whether user is the direct manager of the given employee_id.

    This uses the manager_id embedded in the user's JWT (set from the User.manager_id
    column at login time — but that is the user's own manager, not their reports).

    The reliable check is whether the resource's employee has manager_id == user.id.
    We rely on the caller to pass the correct employee_id of the resource.

    In all call sites, we compare user.id against the resource's manager_id column,
    not via this helper. This helper is kept for explicit relationship checks where
    we receive the employee's reported manager_id.
    """
    return str(user.id) == str(employee_id)


# ── Public API ─────────────────────────────────────────────────────────────────

def can(user: "CurrentUser", action: str, resource: Any = None) -> bool:
    """
    Evaluate policy-based authorization.

    Parameters
    ----------
    user     : CurrentUser — the authenticated user context (from JWT).
    action   : str — dot-separated action, e.g. "review.approve".
    resource : Any — optional ORM resource object for resource-level checks.

    Returns True iff access is permitted. Defaults to deny.
    """
    # Guard: inactive users are never permitted anything
    # CurrentUser doesn't carry is_active; that check is done at login (auth_service).
    # We trust that only active users receive valid JWTs.

    # 1. Tenant Isolation — Hard Boundary
    # Any resource that belongs to an organization must match the user's org.
    if resource is not None:
        resource_org_id = _resolve_organization_id(resource)
        if resource_org_id is not None:
            user_org_id = str(user.organization_id) if user.organization_id else None
            if user_org_id is None or user_org_id != resource_org_id:
                logger.warning(
                    "authz_tenant_mismatch user_id=%s user_org=%s resource_org=%s action=%s",
                    str(user.id), user_org_id, resource_org_id, action,
                )
                return False

    # 2. Action Routing
    try:
        resource_type, op = action.split(".", 1)
    except ValueError:
        logger.error("authz_invalid_action_format: %s", action)
        return False

    dispatch = {
        "people":       _evaluate_people_policy,
        "review_cycle": _evaluate_review_cycle_policy,
        "review":       _evaluate_review_policy,
        "report":       _evaluate_report_policy,
        "goal":         _evaluate_goal_policy,
        "feedback":     _evaluate_feedback_policy,
        "insight":      _evaluate_insight_policy,
        "export":       _evaluate_export_policy,
    }

    handler = dispatch.get(resource_type)
    if handler is None:
        logger.warning("authz_unknown_resource_type: %s", action)
        return False

    result = handler(user, op, resource)
    if not result:
        logger.info(
            "authz_denied user_id=%s role=%s action=%s",
            str(user.id), user.role.value, action,
        )
    return result


# ── Policy Handlers ────────────────────────────────────────────────────────────

def _evaluate_people_policy(user: "CurrentUser", op: str, resource: Any) -> bool:
    """
    people.create  → admin only
    people.read    → any user in same org (collection); own record or manager's reports
    people.update  → admin only, or self-update
    people.delete  → admin only
    """
    if _is_admin(user):
        return True

    if op == "read":
        if resource is None:
            # Collection-level: listing users in the org — allowed for all authenticated
            return True
        # Individual record: own profile, or manager reading a direct report
        if str(resource.id) == str(user.id):
            return True
        if user.role == UserRole.MANAGER:
            # Manager can read employees whose manager_id is the current user
            if hasattr(resource, "manager_id") and resource.manager_id is not None:
                return str(resource.manager_id) == str(user.id)
        return False

    if op == "update":
        # Only self or admin
        return resource is not None and str(resource.id) == str(user.id)

    # create / delete: admin only (handled above)
    return False


def _evaluate_review_cycle_policy(user: "CurrentUser", op: str, resource: Any) -> bool:
    """
    review_cycle.create → manager or admin
    review_cycle.read   → any in org (collection); member of cycle (individual)
    review_cycle.update → admin only (status transitions)
    review_cycle.delete → admin only
    """
    if _is_admin(user):
        return True

    if op == "create":
        return user.role == UserRole.MANAGER

    if op == "read":
        # Any authenticated user can list/read cycles in their org
        return True

    if op == "update":
        # Only admin can update cycle status; managers cannot
        return False

    # delete: admin only
    return False


def _evaluate_review_policy(user: "CurrentUser", op: str, resource: Any) -> bool:
    """
    review.create      → manager or admin
    review.read        → admin, or the employee/manager on the review
    review.update      → admin, or the employee (to submit their own), or manager
    review.submit      → employee (own review) or manager
    review.approve     → manager of that specific review, or admin
    review.acknowledge → employee only (their own review)
    review.delete      → admin only
    """
    if _is_admin(user):
        return True

    if op == "create":
        return user.role == UserRole.MANAGER

    if op == "read":
        if resource is None:
            return True  # Collection access — filtered by repository
        return (
            str(getattr(resource, "employee_id", None)) == str(user.id)
            or str(getattr(resource, "manager_id", None)) == str(user.id)
        )

    if op in ("update", "submit"):
        if resource is None:
            return user.role == UserRole.MANAGER
        # Manager of this review, or the employee submitting their own
        return (
            str(getattr(resource, "manager_id", None)) == str(user.id)
            or str(getattr(resource, "employee_id", None)) == str(user.id)
        )

    if op == "approve":
        if resource is None:
            return False
        # Only the specific manager assigned to this review can approve
        return str(getattr(resource, "manager_id", None)) == str(user.id)

    if op == "acknowledge":
        if resource is None:
            return False
        # Only the employee of this specific review can acknowledge
        return str(getattr(resource, "employee_id", None)) == str(user.id)

    # delete: admin only
    return False


def _evaluate_report_policy(user: "CurrentUser", op: str, resource: Any) -> bool:
    """
    report.read    → admin; manager of the review; employee (finalized only)
    report.approve → admin; manager of the review
    report.update  → admin; manager of the review
    """
    if _is_admin(user):
        return True

    if resource is None:
        # Collection access — caller must scope by org
        return user.role in (UserRole.MANAGER, UserRole.EMPLOYEE)

    # Resolve the underlying review
    review = getattr(resource, "review", None)
    if review is None:
        # Cannot determine ownership without the review
        logger.warning("authz_report_no_review report_id=%s", str(getattr(resource, "id", "unknown")))
        return False

    if op == "read":
        if user.role == UserRole.MANAGER:
            return str(getattr(review, "manager_id", None)) == str(user.id)
        if user.role == UserRole.EMPLOYEE:
            from models.enums import ReportStatus
            is_own = str(getattr(review, "employee_id", None)) == str(user.id)
            is_finalized = getattr(resource, "status", None) == ReportStatus.FINALIZED
            return is_own and is_finalized
        return False

    if op in ("approve", "update"):
        if user.role == UserRole.MANAGER:
            return str(getattr(review, "manager_id", None)) == str(user.id)
        return False

    return False


def _evaluate_goal_policy(user: "CurrentUser", op: str, resource: Any) -> bool:
    """
    goal.create → admin, or employee (for themselves)
    goal.read   → admin, or owner, or their direct manager
    goal.update → admin, or owner
    goal.delete → admin, or owner
    """
    if _is_admin(user):
        return True

    if op == "read":
        if resource is None:
            return True  # Collection — filtered by repository
        employee_id = str(getattr(resource, "employee_id", None))
        if employee_id == str(user.id):
            return True
        # Manager can read goals of their direct reports
        if user.role == UserRole.MANAGER:
            # We check via the resource's employee's manager_id if available
            employee = getattr(resource, "employee", None)
            if employee and hasattr(employee, "manager_id") and employee.manager_id is not None:
                return str(employee.manager_id) == str(user.id)
        return False

    if op in ("create", "update", "delete"):
        if resource is None:
            return True  # Will be validated on actual resource
        return str(getattr(resource, "employee_id", None)) == str(user.id)

    return False


def _evaluate_feedback_policy(user: "CurrentUser", op: str, resource: Any) -> bool:
    """
    feedback.create → any authenticated user
    feedback.read   → admin, author, recipient, or recipient's manager
    feedback.update → admin or author
    feedback.delete → admin or author
    """
    if _is_admin(user):
        return True

    if op == "create":
        return True

    if op == "read":
        if resource is None:
            return True  # Collection — filtered by repository
        is_author = str(getattr(resource, "author_id", None)) == str(user.id)
        is_recipient = str(getattr(resource, "recipient_id", None)) == str(user.id)
        if is_author or is_recipient:
            return True
        # Manager can read feedback received by their direct reports
        if user.role == UserRole.MANAGER:
            recipient = getattr(resource, "recipient", None)
            if recipient and hasattr(recipient, "manager_id") and recipient.manager_id is not None:
                return str(recipient.manager_id) == str(user.id)
        return False

    if op in ("update", "delete"):
        return resource is not None and str(getattr(resource, "author_id", None)) == str(user.id)

    return False


def _evaluate_insight_policy(user: "CurrentUser", op: str, resource: Any) -> bool:
    """
    insight.read     → admin, or owner/manager of the underlying resource
    insight.generate → manager or admin
    """
    if _is_admin(user):
        return True

    if op == "read":
        if resource is None:
            return True
        if hasattr(resource, "employee_id"):
            if str(resource.employee_id) == str(user.id):
                return True
            if user.role == UserRole.MANAGER:
                employee = getattr(resource, "employee", None)
                if employee and hasattr(employee, "manager_id") and employee.manager_id is not None:
                    return str(employee.manager_id) == str(user.id)
        return False

    if op == "generate":
        return user.role == UserRole.MANAGER

    return False


def _evaluate_export_policy(user: "CurrentUser", op: str, resource: Any) -> bool:
    """
    export.read  → admin; manager of the review; employee for their own finalized reports
    """
    if _is_admin(user):
        return True

    if op == "read":
        if resource is None:
            return user.role in (UserRole.MANAGER, UserRole.EMPLOYEE)
        # resource is a Report or ReportExport — delegate to report policy
        return _evaluate_report_policy(user, "read", resource)

    return False
