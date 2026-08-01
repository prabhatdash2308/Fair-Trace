"""ReviewGuard AI — User Repository"""

from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session

from models.db.user import User
from repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, db: Session, email: str) -> User | None:
        return db.scalar(select(User).where(User.email == email))

    def get_direct_reports(self, db: Session, manager_id: UUID) -> list[User]:
        return list(db.scalars(select(User).where(User.manager_id == manager_id)).all())

    def list_all_active(self, db: Session, skip: int = 0, limit: int = 50) -> tuple[list[User], int]:
        return self.list_paginated(db, skip, limit, filters={"is_active": True})


user_repo = UserRepository()
