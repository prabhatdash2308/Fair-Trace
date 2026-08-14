"""FairTrace — Authorization Service"""

from typing import Any
from models.db.user import User
from models.enums import UserRole
import logging

logger = logging.getLogger(__name__)

class AuthorizationError(Exception):
    pass

def _resolve_organization_id(resource: Any) -> str | None:
    """Safely extract organization_id from a resource (or its parent)."""
    if not resource:
        return None
    if hasattr(resource, "organization_id"):
        return str(resource.organization_id)
    # E.g. Report -> Review -> organization_id
    if hasattr(resource, "review") and resource.review:
        return str(resource.review.organization_id)
    # E.g. ReviewInput -> Review -> organization_id
    if hasattr(resource, "review") and resource.review:
        return str(resource.review.organization_id)
    return None

def can(user: User, action: str, resource: Any = None) -> bool:
    """
    Evaluate policy-based authorization.
    Supports resource-aware rules (e.g. ownership, tenant scoping).
    """
    if not user.is_active:
        logger.warning(f"Authz denied: User {user.id} is inactive.")
        return False

    # 1. Tenant Isolation (Hard Boundary)
    # If the resource belongs to an organization, it MUST match the user's organization.
    if resource:
        resource_org_id = _resolve_organization_id(resource)
        if resource_org_id and str(user.organization_id) != resource_org_id:
            logger.warning(f"Authz denied: Tenant mismatch. User {user.organization_id} vs Resource {resource_org_id}")
            return False

    # 2. Action Routing
    try:
        resource_type, op = action.split(".")
    except ValueError:
        logger.error(f"Authz denied: Invalid action format {action}")
        return False

    if resource_type == "people":
        return _evaluate_people_policy(user, op, resource)
    elif resource_type == "goal":
        return _evaluate_goal_policy(user, op, resource)
    elif resource_type == "feedback":
        return _evaluate_feedback_policy(user, op, resource)
    elif resource_type == "review":
        return _evaluate_review_policy(user, op, resource)
    elif resource_type == "report":
        return _evaluate_report_policy(user, op, resource)
    elif resource_type == "insight":
        return _evaluate_insight_policy(user, op, resource)

    # Deny by default
    logger.warning(f"Authz denied: Unknown action {action}")
    return False

def _evaluate_people_policy(user: User, op: str, resource: Any) -> bool:
    if user.role in (UserRole.ORG_ADMIN, UserRole.SUPER_ADMIN, UserRole.HR_ADMIN):
        return True
    
    if op == "read":
        # Any active user can read people in their org
        return True
    if op == "update":
        # Only self or admin can update
        return resource and str(resource.id) == str(user.id)
    return False

def _evaluate_goal_policy(user: User, op: str, resource: Any) -> bool:
    if user.role in (UserRole.ORG_ADMIN, UserRole.SUPER_ADMIN, UserRole.HR_ADMIN):
        return True
    
    if op == "read":
        if not resource:
            return True # Collection access check (handled by repository filter)
        # Owner or Manager
        return str(resource.employee_id) == str(user.id) or _is_manager_of(user, resource.employee_id)
    
    if op in ["create", "update", "delete"]:
        if not resource:
            return True
        # Only owner or admin can mutate goals
        return str(resource.employee_id) == str(user.id)
    
    return False

def _evaluate_feedback_policy(user: User, op: str, resource: Any) -> bool:
    if user.role in (UserRole.ORG_ADMIN, UserRole.SUPER_ADMIN, UserRole.HR_ADMIN):
        return True
        
    if op == "read":
        if not resource:
            return True
        # For P2.4 this will be expanded with FeedbackVisibility. 
        # For now, recipient, author, or recipient's manager can read.
        is_recipient = str(resource.recipient_id) == str(user.id)
        is_author = str(resource.author_id) == str(user.id)
        is_manager = _is_manager_of(user, resource.recipient_id)
        return is_recipient or is_author or is_manager
        
    if op == "create":
        return True
    
    if op == "delete":
        # Only author or admin can delete
        return resource and str(resource.author_id) == str(user.id)
        
    return False

def _evaluate_review_policy(user: User, op: str, resource: Any) -> bool:
    if user.role in (UserRole.ORG_ADMIN, UserRole.SUPER_ADMIN, UserRole.HR_ADMIN):
        return True
        
    if op == "read":
        if not resource:
            return True
        is_employee = str(resource.employee_id) == str(user.id)
        is_manager = str(resource.manager_id) == str(user.id)
        return is_employee or is_manager
        
    if op == "create":
        # Only manager or admin can create reviews
        return user.role == UserRole.MANAGER
        
    if op == "approve":
        # Only manager or admin can approve
        if not resource:
            return False
        return str(resource.manager_id) == str(user.id)
        
    return False

def _evaluate_report_policy(user: User, op: str, resource: Any) -> bool:
    if not resource:
        return user.role in [UserRole.ADMIN, UserRole.MANAGER]
    # Defer to review policy
    return _evaluate_review_policy(user, op, resource.review)

def _evaluate_insight_policy(user: User, op: str, resource: Any) -> bool:
    if user.role in (UserRole.ORG_ADMIN, UserRole.SUPER_ADMIN, UserRole.HR_ADMIN):
        return True
        
    if op == "read":
        if not resource:
            return True
        # E.g. reading an insight requires reading the underlying review/person
        if hasattr(resource, "employee_id"):
            return str(resource.employee_id) == str(user.id) or _is_manager_of(user, resource.employee_id)
    
    if op == "generate":
        # Typically background agents or explicit manager/admin action
        return user.role == UserRole.MANAGER
        
    return False

def _is_manager_of(user: User, employee_id: str) -> bool:
    """Helper to check if user manages the employee. 
    Note: A full check might require querying the DB. 
    For simple cases, if this is called, we assume the caller passes the check or we just check if role is MANAGER (which is a loose check).
    In a real system, we'd need the DB session to resolve the org tree, OR we trust the org_id + manager role for now."""
    if user.role != UserRole.MANAGER:
        return False
    # P2 Improvement: Actually check DB relationship if needed, 
    # but for now we rely on the repository to filter by `manager_id`.
    return True
