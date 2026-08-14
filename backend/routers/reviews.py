"""FairTrace — Reviews Router"""

from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from dependencies import CurrentUser, get_current_user, get_db, require_manager_or_admin
from models.schemas import (
    ReviewCreate,
    ReviewResponse,
    InputSubmit,
    InputResponse,
)
from services import review_service


reviews_router = APIRouter()


@reviews_router.post("", response_model=ReviewResponse, status_code=201,
                    summary="Create Review", tags=["Reviews"])
def create_review(
    body: ReviewCreate,
    db: Session = Depends(get_db),
    actor: CurrentUser = Depends(require_manager_or_admin),
):
    return review_service.create_review(db, body, actor)


@reviews_router.get("", summary="List Reviews", tags=["Reviews"])
def list_reviews(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    actor: CurrentUser = Depends(get_current_user),
):
    items, total = review_service.list_reviews(db, actor, skip, limit)
    return {
        "items": [ReviewResponse.model_validate(r) for r in items],
        "total": total,
        "skip": skip,
        "limit": limit,
        "has_more": skip + limit < total,
    }


@reviews_router.get("/{review_id}", response_model=ReviewResponse, summary="Get Review", tags=["Reviews"])
def get_review(
    review_id: UUID,
    db: Session = Depends(get_db),
    actor: CurrentUser = Depends(get_current_user),
):
    return review_service.get_review(db, review_id, actor)


@reviews_router.post("/{review_id}/submit", response_model=ReviewResponse, summary="Submit for Manager Review", tags=["Reviews"])
def submit_for_manager_review(
    review_id: UUID,
    db: Session = Depends(get_db),
    actor: CurrentUser = Depends(get_current_user),
):
    return review_service.submit_for_manager_review(db, review_id, actor)


@reviews_router.post("/{review_id}/approve", response_model=ReviewResponse, summary="Approve Review", tags=["Reviews"])
def approve_review(
    review_id: UUID,
    db: Session = Depends(get_db),
    actor: CurrentUser = Depends(get_current_user),
):
    return review_service.approve(db, review_id, actor)


@reviews_router.post("/{review_id}/request-revision", response_model=ReviewResponse, summary="Request Revision", tags=["Reviews"])
def request_revision(
    review_id: UUID,
    db: Session = Depends(get_db),
    actor: CurrentUser = Depends(get_current_user),
):
    return review_service.request_revision(db, review_id, actor)


@reviews_router.post("/{review_id}/acknowledge", response_model=ReviewResponse, summary="Acknowledge Review", tags=["Reviews"])
def acknowledge_review(
    review_id: UUID,
    db: Session = Depends(get_db),
    actor: CurrentUser = Depends(get_current_user),
):
    return review_service.acknowledge(db, review_id, actor)


@reviews_router.post("/{review_id}/complete", response_model=ReviewResponse, summary="Complete Review", tags=["Reviews"])
def complete_review(
    review_id: UUID,
    db: Session = Depends(get_db),
    actor: CurrentUser = Depends(get_current_user),
):
    return review_service.complete(db, review_id, actor)


@reviews_router.post("/{review_id}/inputs", response_model=InputResponse, status_code=201, summary="Submit Review Input", tags=["Reviews"])
def submit_input(
    review_id: UUID,
    body: InputSubmit,
    db: Session = Depends(get_db),
    actor: CurrentUser = Depends(get_current_user),
):
    return review_service.submit_input(db, review_id, body, actor)
