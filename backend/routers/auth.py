"""ReviewGuard AI — Auth Router"""

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from dependencies import get_db
from models.schemas import LoginRequest, TokenResponse
from services.auth_service import authenticate_user, create_token_for_user
from repositories import audit_repo
from models.enums import AuditEventType

router = APIRouter()


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Authenticate User",
    description="Returns a signed JWT on successful login. Same error for wrong email or wrong password (anti-enumeration).",
    responses={
        200: {"description": "JWT returned"},
        401: {"description": "Invalid credentials"},
    },
)
def login(request: Request, body: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, body.email, body.password)
    audit_repo.create(db, {
        "event_type": AuditEventType.USER_LOGIN,
        "actor_id": user.id,
        "actor_role": user.role,
        "resource_type": "user",
        "resource_id": user.id,
        "event_payload": {"email": user.email},
        "ip_address": request.client.host if request.client else None,
        "correlation_id": getattr(request.state, "correlation_id", None),
    })
    db.commit()
    return create_token_for_user(user)
