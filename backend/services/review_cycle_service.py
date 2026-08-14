"""FairTrace — Review Cycle Service"""

from uuid import UUID
from sqlalchemy.orm import Session
from core.exceptions import BusinessValidationError, ConflictError, ForbiddenError, NotFoundError, InvalidStateError
from dependencies import CurrentUser
from models.db.review_cycle import ReviewCycle
from models.enums import ReviewCycleStatus, AuditEventType, UserRole
from models.schemas import ReviewCycleCreate
from repositories import review_cycle_repo, audit_repo, user_repo
from services.authz_service import can


def create_cycle(db: Session, data: ReviewCycleCreate, actor: CurrentUser) -> ReviewCycle:
    if not can(actor, "review_cycle.create"):
        raise ForbiddenError("You do not have permission to create review cycles.")

    if data.end_date <= data.start_date:
        raise BusinessValidationError("Review period end must be after start date.")

    cycle = review_cycle_repo.create(db, {
        "title": data.title,
        "organization_id": actor.organization_id,
        "start_date": data.start_date,
        "end_date": data.end_date,
        "status": ReviewCycleStatus.DRAFT,
    })
    
    audit_repo.create(db, {
        "event_type": AuditEventType.REVIEW_CYCLE_CREATED,
        "actor_id": actor.id,
        "actor_role": actor.role,
        "resource_type": "review_cycle",
        "resource_id": cycle.id,
        "event_payload": {"title": data.title},
    })
    db.commit()
    db.refresh(cycle)
    return cycle


def get_cycle(db: Session, cycle_id: UUID, actor: CurrentUser) -> ReviewCycle:
    cycle = review_cycle_repo.get_by_id(db, cycle_id, organization_id=actor.organization_id)
    if not cycle:
        raise NotFoundError(f"Review cycle {cycle_id} not found.")
    
    if not can(actor, "review_cycle.read", cycle):
        raise ForbiddenError("You do not have access to this review cycle.")
        
    return cycle


def activate_cycle(db: Session, cycle_id: UUID, actor: CurrentUser) -> ReviewCycle:
    cycle = get_cycle(db, cycle_id, actor)
    
    if not can(actor, "review_cycle.update", cycle):
        raise ForbiddenError("You do not have permission to update this review cycle.")
        
    if cycle.status != ReviewCycleStatus.DRAFT:
        raise InvalidStateError("Only DRAFT cycles can be activated.")
        
    cycle = review_cycle_repo.update_status(db, cycle, ReviewCycleStatus.ACTIVE)
    
    audit_repo.create(db, {
        "event_type": AuditEventType.REVIEW_CYCLE_UPDATED,
        "actor_id": actor.id,
        "actor_role": actor.role,
        "resource_type": "review_cycle",
        "resource_id": cycle.id,
        "event_payload": {"old_status": ReviewCycleStatus.DRAFT.value, "new_status": ReviewCycleStatus.ACTIVE.value},
    })
    db.commit()
    db.refresh(cycle)
    return cycle


def complete_cycle(db: Session, cycle_id: UUID, actor: CurrentUser) -> ReviewCycle:
    cycle = get_cycle(db, cycle_id, actor)
    
    if not can(actor, "review_cycle.update", cycle):
        raise ForbiddenError("You do not have permission to update this review cycle.")
        
    if cycle.status != ReviewCycleStatus.ACTIVE:
        raise InvalidStateError("Only ACTIVE cycles can be completed.")
        
    cycle = review_cycle_repo.update_status(db, cycle, ReviewCycleStatus.COMPLETED)
    
    audit_repo.create(db, {
        "event_type": AuditEventType.REVIEW_CYCLE_UPDATED,
        "actor_id": actor.id,
        "actor_role": actor.role,
        "resource_type": "review_cycle",
        "resource_id": cycle.id,
        "event_payload": {"old_status": ReviewCycleStatus.ACTIVE.value, "new_status": ReviewCycleStatus.COMPLETED.value},
    })
    db.commit()
    db.commit()
    db.refresh(cycle)
    return cycle

def list_cycles(db: Session, actor: CurrentUser, skip: int = 0, limit: int = 20) -> tuple[list[ReviewCycle], int]:
    if not can(actor, "review_cycle.read"):
        raise ForbiddenError("You do not have permission to view review cycles.")
    return review_cycle_repo.list_paginated(db, skip, limit, organization_id=actor.organization_id)

def update_status(db: Session, cycle_id: UUID, new_status: ReviewCycleStatus, actor: CurrentUser) -> ReviewCycle:
    if new_status == ReviewCycleStatus.ACTIVE:
        return activate_cycle(db, cycle_id, actor)
    elif new_status == ReviewCycleStatus.COMPLETED:
        return complete_cycle(db, cycle_id, actor)
    else:
        raise BusinessValidationError(f"Cannot transition to {new_status}")
