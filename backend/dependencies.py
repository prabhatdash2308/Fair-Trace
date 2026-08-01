"""
ReviewGuard AI — FastAPI Dependency Injection
All Depends() factory functions are defined here and imported by routers.
"""

from dataclasses import dataclass
from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from core.database import get_db_session
from core.exceptions import ForbiddenError, InvalidTokenError
from core.security import verify_token
from models.enums import UserRole

# OAuth2 scheme — tokenUrl matches the login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


@dataclass
class CurrentUser:
    """Authenticated user context extracted from JWT."""
    id: UUID
    email: str
    role: UserRole
    full_name: str
    manager_id: UUID | None = None


# ── Session Dependency ─────────────────────────────────────────────────────────

def get_db() -> Session:
    """Yields a database session. Alias for get_db_session."""
    yield from get_db_session()


# ── Authentication Dependency ──────────────────────────────────────────────────

def get_current_user(
    token: str | None = Depends(oauth2_scheme),
) -> CurrentUser:
    """
    Validates JWT and returns the authenticated user context.
    Raises InvalidTokenError (401) if token is missing or invalid.
    """
    if not token:
        raise InvalidTokenError("No authentication token provided.")

    payload = verify_token(token)

    return CurrentUser(
        id=UUID(payload["sub"]),
        email=payload["email"],
        role=UserRole(payload["role"]),
        full_name=payload["full_name"],
        manager_id=UUID(payload["manager_id"]) if payload.get("manager_id") else None,
    )


# ── Role Guard Dependencies ────────────────────────────────────────────────────

def require_admin(
    current_user: CurrentUser = Depends(get_current_user),
) -> CurrentUser:
    """Requires ADMIN role. Raises ForbiddenError (403) otherwise."""
    if current_user.role != UserRole.ADMIN:
        raise ForbiddenError("This action requires ADMIN privileges.")
    return current_user


def require_manager(
    current_user: CurrentUser = Depends(get_current_user),
) -> CurrentUser:
    """Requires MANAGER role exactly. Use require_manager_or_admin for broader access."""
    if current_user.role != UserRole.MANAGER:
        raise ForbiddenError("This action requires MANAGER privileges.")
    return current_user


def require_manager_or_admin(
    current_user: CurrentUser = Depends(get_current_user),
) -> CurrentUser:
    """Requires MANAGER or ADMIN role."""
    if current_user.role not in (UserRole.MANAGER, UserRole.ADMIN):
        raise ForbiddenError("This action requires MANAGER or ADMIN privileges.")
    return current_user


def require_any_authenticated(
    current_user: CurrentUser = Depends(get_current_user),
) -> CurrentUser:
    """Any authenticated user (ADMIN, MANAGER, EMPLOYEE)."""
    return current_user
