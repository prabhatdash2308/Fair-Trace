"""
ReviewGuard AI — Database Engine and Session Management
Single source of truth for all SQLAlchemy configuration.
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config import settings

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,          # Verify connections before use
    pool_size=10,
    max_overflow=20,
    echo=settings.is_development, # Log SQL in development only
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db_session() -> Generator[Session, None, None]:
    """
    FastAPI dependency that yields a database session.
    Ensures session is closed after request completes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
