"""
ReviewGuard AI — JWT Authentication & Password Hashing
All cryptographic operations are centralized here.
"""

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from config import settings
from core.exceptions import InvalidTokenError

# bcrypt context — cost factor 12
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)


def hash_password(plain_password: str) -> str:
    """Returns a bcrypt hash of the plain password."""
    return _pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Timing-safe comparison of plain password against stored bcrypt hash.
    Returns True if they match.
    """
    return _pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict[str, Any]) -> str:
    """
    Creates a signed JWT token.

    Required keys in data:
        sub       - user UUID (as string)
        email     - user email
        role      - user role string
        full_name - user display name

    Returns: signed JWT string
    """
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=settings.jwt_expire_hours)
    payload.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    })
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def verify_token(token: str) -> dict[str, Any]:
    """
    Validates JWT signature and expiry.

    Raises:
        InvalidTokenError — if token is missing, malformed, or expired.

    Returns:
        Decoded payload dict containing sub, email, role, full_name.
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        user_id: str | None = payload.get("sub")
        if not user_id:
            raise InvalidTokenError("Token payload missing 'sub' claim.")
        return payload
    except JWTError as exc:
        raise InvalidTokenError(str(exc)) from exc
