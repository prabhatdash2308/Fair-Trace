"""FairTrace — People Service"""

from uuid import UUID
from sqlalchemy.orm import Session
from core.exceptions import ConflictError, NotFoundError, ForbiddenError
from core.security import hash_password
from dependencies import CurrentUser
from models.db.user import User
from models.schemas import UserCreate
from repositories import user_repo
from services.authz_service import can


def create_user(db: Session, data: UserCreate, actor: CurrentUser) -> User:
    if not can(actor, "people.create"):
        raise ForbiddenError("You do not have permission to create users.")
        
    existing = user_repo.get_by_email(db, data.email)
    if existing:
        raise ConflictError(f"A user with email '{data.email}' already exists.")

    user = user_repo.create(db, {
        "email": data.email,
        "password_hash": hash_password(data.password),
        "full_name": data.full_name,
        "role": data.role,
        "manager_id": data.manager_id,
        "organization_id": actor.organization_id,
        "is_active": True,
    })
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id: UUID, actor: CurrentUser) -> User:
    user = user_repo.get_by_id(db, user_id, organization_id=actor.organization_id)
    if not user:
        raise NotFoundError(f"User {user_id} not found.")
    
    if not can(actor, "people.read", user):
        raise ForbiddenError("You do not have access to this user's profile.")
        
    return user


def list_users(db: Session, actor: CurrentUser, skip: int = 0, limit: int = 20) -> tuple[list[User], int]:
    if not can(actor, "people.read"):
        raise ForbiddenError("You do not have permission to list users.")
        
    # user_repo list_paginated will handle org isolation when we refactor it or we use filters
    return user_repo.list_paginated(db, skip, limit, filters={"is_active": True}, organization_id=actor.organization_id)
