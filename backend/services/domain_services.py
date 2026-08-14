"""FairTrace — User, ReviewCycle, ReviewInput Services"""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import (
    BusinessValidationError,
    ConflictError,
    ForbiddenError,
    InvalidStateError,
    NotFoundError,
)
from core.security import hash_password
from dependencies import CurrentUser
from models.db.user import User
from models.db.review_cycle import ReviewCycle
from models.db.review_input import ReviewInput
from models.enums import InputType, ReviewCycleStatus, UserRole
from models.schemas import ReviewCycleCreate, UserCreate, InputSubmit
from repositories import audit_repo, review_cycle_repo, review_input_repo, user_repo
from models.enums import AuditEventType


# ── User Service ───────────────────────────────────────────────────────────────

def create_user(db: Session, data: UserCreate, actor: CurrentUser) -> User:
    existing = user_repo.get_by_email(db, data.email)
    if existing:
        raise ConflictError(f"A user with email '{data.email}' already exists.")

    user = user_repo.create(db, {
        "email": data.email,
        "password_hash": hash_password(data.password),
        "full_name": data.full_name,
        "role": data.role,
        "manager_id": data.manager_id,
        "is_active": True,
    })
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id: UUID) -> User:
    user = user_repo.get_by_id(db, user_id)
    if not user:
        raise NotFoundError(f"User {user_id} not found.")
    return user


def list_users(db: Session, skip: int = 0, limit: int = 20) -> tuple[list[User], int]:
    return user_repo.list_all_active(db, skip, limit)


# ── ReviewCycle Service ────────────────────────────────────────────────────────

def create_review_cycle(db: Session, data: ReviewCycleCreate, actor: CurrentUser) -> ReviewCycle:
    # Validate employee exists
    employee = user_repo.get_by_id(db, data.employee_id)
    if not employee:
        raise NotFoundError(f"Employee {data.employee_id} not found.")

    if data.review_period_end <= data.review_period_start:
        raise BusinessValidationError("Review period end must be after start date.")

    # Manager is always the creator if MANAGER role
    manager_id = actor.id if actor.role == UserRole.MANAGER else (
        employee.manager_id or actor.id
    )

    cycle = review_cycle_repo.create(db, {
        "employee_id": data.employee_id,
        "manager_id": manager_id,
        "created_by": actor.id,
        "organization_id": actor.organization_id,
        "title": data.title,
        "review_period_start": data.review_period_start,
        "review_period_end": data.review_period_end,
        "status": ReviewCycleStatus.DRAFT,
    })
    audit_repo.create(db, {
        "event_type": AuditEventType.REVIEW_CYCLE_CREATED,
        "actor_id": actor.id,
        "actor_role": actor.role,
        "resource_type": "review_cycle",
        "resource_id": cycle.id,
        "event_payload": {"title": data.title, "employee_id": str(data.employee_id)},
    })
    db.commit()
    db.refresh(cycle)
    return cycle


def get_review_cycle(db: Session, cycle_id: UUID, actor: CurrentUser) -> ReviewCycle:
    cycle = review_cycle_repo.get_by_id(db, cycle_id)
    if not cycle:
        raise NotFoundError(f"Review cycle {cycle_id} not found.")
    _assert_cycle_access(cycle, actor)
    return cycle


def list_review_cycles(
    db: Session, actor: CurrentUser, skip: int = 0, limit: int = 20
) -> tuple[list[ReviewCycle], int]:
    _ADMIN_ROLES = (UserRole.ORG_ADMIN, UserRole.SUPER_ADMIN, UserRole.HR_ADMIN)
    if actor.role in _ADMIN_ROLES:
        return review_cycle_repo.list_paginated(db, skip, limit)
    if actor.role == UserRole.MANAGER:
        return review_cycle_repo.list_for_manager(db, actor.id, skip, limit)
    return review_cycle_repo.list_for_employee(db, actor.id, skip, limit)


def update_cycle_status(
    db: Session, cycle_id: UUID, new_status: ReviewCycleStatus, actor: CurrentUser
) -> ReviewCycle:
    cycle = review_cycle_repo.get_by_id(db, cycle_id)
    if not cycle:
        raise NotFoundError(f"Review cycle {cycle_id} not found.")
    _assert_cycle_access(cycle, actor)

    old_status = cycle.status
    cycle = review_cycle_repo.update_status(db, cycle, new_status)
    audit_repo.create(db, {
        "event_type": AuditEventType.REVIEW_CYCLE_UPDATED,
        "actor_id": actor.id,
        "actor_role": actor.role,
        "resource_type": "review_cycle",
        "resource_id": cycle.id,
        "event_payload": {"old_status": old_status.value, "new_status": new_status.value},
    })
    db.commit()
    db.refresh(cycle)
    return cycle


def _assert_cycle_access(cycle: ReviewCycle, actor: CurrentUser) -> None:
    _ADMIN_ROLES = (UserRole.ORG_ADMIN, UserRole.SUPER_ADMIN, UserRole.HR_ADMIN)
    if actor.role in _ADMIN_ROLES:
        return
    if actor.role == UserRole.MANAGER and cycle.manager_id == actor.id:
        return
    if actor.role == UserRole.EMPLOYEE and cycle.employee_id == actor.id:
        return
    raise ForbiddenError("You do not have access to this review cycle.")


# ── ReviewInput Service ────────────────────────────────────────────────────────

def submit_input(
    db: Session, cycle_id: UUID, data: InputSubmit, actor: CurrentUser
) -> ReviewInput:
    cycle = review_cycle_repo.get_by_id(db, cycle_id)
    if not cycle:
        raise NotFoundError(f"Review cycle {cycle_id} not found.")
    if cycle.status != ReviewCycleStatus.ACTIVE:
        raise InvalidStateError("Inputs can only be submitted for ACTIVE review cycles.")
    _assert_cycle_access(cycle, actor)

    # Employee cannot submit peer review on their own cycle
    if (actor.role == UserRole.EMPLOYEE
            and cycle.employee_id == actor.id
            and data.input_type == InputType.PEER_REVIEW):
        raise ForbiddenError("Employees cannot submit peer reviews for their own cycle.")

    review_input = review_input_repo.create(db, {
        "review_cycle_id": cycle_id,
        "submitted_by": actor.id,
        "input_type": data.input_type,
        "content_text": data.content_text,
        "is_anonymized": data.is_anonymized,
    })
    audit_repo.create(db, {
        "event_type": AuditEventType.INPUT_SUBMITTED,
        "actor_id": actor.id,
        "actor_role": actor.role,
        "resource_type": "review_input",
        "resource_id": review_input.id,
        "event_payload": {
            "cycle_id": str(cycle_id),
            "input_type": data.input_type.value,
            "char_count": len(data.content_text),
        },
    })
    db.commit()
    db.refresh(review_input)
    return review_input


def list_inputs_for_cycle(
    db: Session, cycle_id: UUID, actor: CurrentUser
) -> list[ReviewInput]:
    cycle = review_cycle_repo.get_by_id(db, cycle_id)
    if not cycle:
        raise NotFoundError(f"Review cycle {cycle_id} not found.")
    _assert_cycle_access(cycle, actor)
    inputs = review_input_repo.list_for_cycle(db, cycle_id)
    # Anonymize peer reviews for EMPLOYEE role
    if actor.role == UserRole.EMPLOYEE:
        for inp in inputs:
            if inp.is_anonymized:
                inp.content_text = "[Content hidden — anonymized peer review]"
    return inputs
