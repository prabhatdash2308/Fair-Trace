"""FairTrace — People Router"""

from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from dependencies import CurrentUser, get_current_user, get_db, require_admin
from models.schemas import UserCreate, UserResponse
from services import people_service


people_router = APIRouter()


@people_router.post("", response_model=UserResponse, status_code=201,
                   summary="Create Person", tags=["People"])
def create_person(
    body: UserCreate,
    db: Session = Depends(get_db),
    actor: CurrentUser = Depends(require_admin),
):
    return people_service.create_user(db, body, actor)


@people_router.get("", summary="List People", tags=["People"])
def list_people(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    actor: CurrentUser = Depends(get_current_user),
):
    items, total = people_service.list_users(db, actor, skip, limit)
    return {
        "items": [UserResponse.model_validate(u) for u in items],
        "total": total,
        "skip": skip,
        "limit": limit,
        "has_more": skip + limit < total,
    }


@people_router.get("/{user_id}", response_model=UserResponse, summary="Get Person", tags=["People"])
def get_person(
    user_id: UUID,
    db: Session = Depends(get_db),
    actor: CurrentUser = Depends(get_current_user),
):
    return people_service.get_user(db, user_id, actor)
