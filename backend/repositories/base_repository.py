"""ReviewGuard AI — Generic Base Repository"""

from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from models.db.base import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    """
    Generic CRUD repository. Entity-specific repositories inherit from this.
    Repositories NEVER call db.commit() — that is the service layer's responsibility.
    """

    def __init__(self, model: type[T]):
        self.model = model

    def get_by_id(self, db: Session, id: UUID) -> T | None:
        return db.get(self.model, id)

    def create(self, db: Session, obj_in: dict) -> T:
        obj = self.model(**obj_in)
        db.add(obj)
        db.flush()
        db.refresh(obj)
        return obj

    def update(self, db: Session, db_obj: T, obj_in: dict) -> T:
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        return db_obj

    def list_paginated(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 20,
        filters: dict | None = None,
    ) -> tuple[list[T], int]:
        stmt = select(self.model)
        if filters:
            for key, value in filters.items():
                stmt = stmt.where(getattr(self.model, key) == value)

        total = db.scalar(select(func.count()).select_from(stmt.subquery()))
        items = db.scalars(stmt.offset(skip).limit(limit)).all()
        return list(items), total or 0
