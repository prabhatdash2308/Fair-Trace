"""FairTrace — Review Service"""

from uuid import UUID
from sqlalchemy.orm import Session
from core.exceptions import BusinessValidationError, ConflictError, ForbiddenError, NotFoundError, InvalidStateError
from dependencies import CurrentUser
from models.db.review import Review
from models.enums import ReviewStatus, AuditEventType, UserRole
from models.schemas import ReviewCreate, InputSubmit
from repositories import review_repo, audit_repo, user_repo
from services.authz_service import can


def create_review(db: Session, data: ReviewCreate, actor: CurrentUser) -> Review:
    if not can(actor, "review.create"):
        raise ForbiddenError("You do not have permission to create reviews.")

    employee = user_repo.get_by_id(db, data.employee_id, organization_id=actor.organization_id)
    if not employee:
        raise NotFoundError(f"Employee {data.employee_id} not found.")

    if data.review_period_end <= data.review_period_start:
        raise BusinessValidationError("Review period end must be after start date.")

    manager_id = actor.id if actor.role == UserRole.MANAGER else (employee.manager_id or actor.id)

    review = review_repo.create(db, {
        "review_cycle_id": data.review_cycle_id,
        "employee_id": data.employee_id,
        "manager_id": manager_id,
        "created_by": actor.id,
        "organization_id": actor.organization_id,
        "title": data.title,
        "review_period_start": data.review_period_start,
        "review_period_end": data.review_period_end,
        "status": ReviewStatus.DRAFT,
    })
    
    audit_repo.create(db, {
        "event_type": AuditEventType.REVIEW_CYCLE_CREATED, # Keep old enum for compatibility
        "actor_id": actor.id,
        "actor_role": actor.role,
        "resource_type": "review",
        "resource_id": review.id,
        "event_payload": {"title": data.title, "employee_id": str(data.employee_id)},
    })
    db.commit()
    db.refresh(review)
    return review


def get_review(db: Session, review_id: UUID, actor: CurrentUser) -> Review:
    review = review_repo.get_with_relations(db, review_id, organization_id=actor.organization_id)
    if not review:
        raise NotFoundError(f"Review {review_id} not found.")
    
    if not can(actor, "review.read", review):
        raise ForbiddenError("You do not have access to this review.")
        
    return review


def list_reviews(db: Session, actor: CurrentUser, skip: int = 0, limit: int = 20) -> tuple[list[Review], int]:
    if actor.role == UserRole.ADMIN:
        return review_repo.list_paginated(db, skip, limit, organization_id=actor.organization_id)
    if actor.role == UserRole.MANAGER:
        return review_repo.list_for_manager(db, actor.id, skip, limit, organization_id=actor.organization_id)
    return review_repo.list_for_employee(db, actor.id, skip, limit, organization_id=actor.organization_id)


def submit_for_manager_review(db: Session, review_id: UUID, actor: CurrentUser) -> Review:
    review = get_review(db, review_id, actor)
    
    if review.status != ReviewStatus.DRAFT:
        raise InvalidStateError(f"Cannot submit review from state {review.status.value}")
        
    if not can(actor, "review.update", review):
        raise ForbiddenError("You do not have permission to submit this review.")
        
    return _transition_review(db, review, ReviewStatus.MANAGER_REVIEW, actor)

def request_revision(db: Session, review_id: UUID, actor: CurrentUser) -> Review:
    review = get_review(db, review_id, actor)
    
    if review.status != ReviewStatus.PENDING_APPROVAL:
        raise InvalidStateError(f"Cannot request revision from state {review.status.value}")
        
    if not can(actor, "review.approve", review):
        raise ForbiddenError("You do not have permission to request revision.")
        
    return _transition_review(db, review, ReviewStatus.REVISION_REQUESTED, actor)

def approve(db: Session, review_id: UUID, actor: CurrentUser) -> Review:
    review = get_review(db, review_id, actor)
    
    if review.status != ReviewStatus.PENDING_APPROVAL:
        raise InvalidStateError(f"Cannot approve review from state {review.status.value}")
        
    if not can(actor, "review.approve", review):
        raise ForbiddenError("You do not have permission to approve this review.")
        
    return _transition_review(db, review, ReviewStatus.APPROVED, actor)

def acknowledge(db: Session, review_id: UUID, actor: CurrentUser) -> Review:
    review = get_review(db, review_id, actor)
    
    if review.status != ReviewStatus.APPROVED:
        raise InvalidStateError(f"Cannot acknowledge review from state {review.status.value}")
        
    if str(review.employee_id) != str(actor.id):
        raise ForbiddenError("Only the employee can acknowledge their review.")
        
    return _transition_review(db, review, ReviewStatus.EMPLOYEE_ACKNOWLEDGED, actor)

def complete(db: Session, review_id: UUID, actor: CurrentUser) -> Review:
    review = get_review(db, review_id, actor)
    
    if review.status not in [ReviewStatus.EMPLOYEE_ACKNOWLEDGED, ReviewStatus.APPROVED]:
        raise InvalidStateError(f"Cannot complete review from state {review.status.value}")
        
    if not can(actor, "review.update", review):
        raise ForbiddenError("You do not have permission to complete this review.")
        
    return _transition_review(db, review, ReviewStatus.COMPLETED, actor)

def _transition_review(db: Session, review: Review, new_status: ReviewStatus, actor: CurrentUser) -> Review:
    if review.status == ReviewStatus.COMPLETED:
        raise InvalidStateError("Completed reviews are immutable.")
        
    old_status = review.status
    review = review_repo.update_status(db, review, new_status)
    
    audit_repo.create(db, {
        "event_type": AuditEventType.REVIEW_CYCLE_UPDATED,
        "actor_id": actor.id,
        "actor_role": actor.role,
        "resource_type": "review",
        "resource_id": review.id,
        "event_payload": {"old_status": old_status.value, "new_status": new_status.value},
    })
    db.commit()
    db.refresh(review)
    return review

def submit_input(db: Session, review_id: UUID, data: InputSubmit, actor: CurrentUser):
    from models.db.review_input import ReviewInput
    from repositories import review_input_repo
    review = get_review(db, review_id, actor)
    
    if review.status != ReviewStatus.DRAFT:
        raise InvalidStateError("Can only submit inputs when review is in DRAFT state.")

    review_input = review_input_repo.create(db, {
        "review_id": review.id,
        "input_type": data.input_type,
        "content_text": data.content_text,
        "is_anonymized": data.is_anonymized,
        "submitted_by": actor.id,
    })
    
    audit_repo.create(db, {
        "event_type": AuditEventType.REVIEW_INPUT_SUBMITTED,
        "actor_id": actor.id,
        "actor_role": actor.role,
        "resource_type": "review",
        "resource_id": review.id,
        "event_payload": {"input_type": data.input_type.value},
    })
    db.commit()
    db.refresh(review_input)
    return review_input

def list_inputs_for_review(db: Session, review_id: UUID, actor: CurrentUser):
    from models.enums import UserRole
    from repositories import review_input_repo
    review = get_review(db, review_id, actor)
    
    inputs = review_input_repo.list_for_cycle(db, review_id)
    # Anonymize peer reviews for EMPLOYEE role
    if actor.role == UserRole.EMPLOYEE:
        for inp in inputs:
            if inp.is_anonymized:
                inp.content_text = "[Content hidden — anonymized peer review]"
    return inputs
