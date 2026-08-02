"""ReviewGuard AI — Auth Service"""

from datetime import timedelta

from sqlalchemy.orm import Session

from config import settings
from core.exceptions import AuthenticationFailedError
from core.security import create_access_token, verify_password
from models.db.user import User
from repositories.user_repository import user_repo


def authenticate_user(db: Session, email: str, password: str) -> User:
    """
    Validates credentials and returns the User on success.
    Raises AuthenticationFailedError on any failure (constant-time — no email enumeration).
    """
    user = user_repo.get_by_email(db, email)
    # A structurally valid dummy bcrypt hash (cost 12) to prevent passlib from crashing.
    dummy_hash = "$2b$12$w.yI/K73o8R9l8xP3zOqI.jJ44y6kQ9X54x3W2k3q3M32v7R7v66O"
    pwd_hash = user.password_hash if user else dummy_hash
    valid = verify_password(password, pwd_hash)

    if not user or not valid or not user.is_active:
        raise AuthenticationFailedError()

    return user


def create_token_for_user(user: User) -> dict:
    """Returns the token response payload for a given user."""
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "role": user.role.value,
        "full_name": user.full_name,
        "manager_id": str(user.manager_id) if user.manager_id else None,
    }
    access_token = create_access_token(token_data)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.jwt_expire_hours * 3600,
        "user": {
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role.value,
        },
    }
