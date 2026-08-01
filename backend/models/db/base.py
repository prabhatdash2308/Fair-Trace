"""
ReviewGuard AI — SQLAlchemy Base and TimestampMixin
All ORM models inherit from Base + TimestampMixin.
"""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    """Provides created_at and updated_at on all models that inherit it."""

    created_at: datetime = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: datetime = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
