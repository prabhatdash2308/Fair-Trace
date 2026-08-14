"""FairTrace — Auth Router"""

import traceback

import structlog
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from dependencies import get_db
from models.schemas import LoginRequest, TokenResponse
from services.auth_service import authenticate_user, create_token_for_user
from repositories import audit_repo
from models.enums import AuditEventType
from core.exceptions import FairTraceException

logger = structlog.get_logger(__name__)

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
    request_id = getattr(request.state, "correlation_id", None)
    ip = request.client.host if request.client else None

    logger.info("login_attempt", email=body.email, ip=ip, request_id=request_id)

    try:
        user = authenticate_user(db, body.email, body.password)
    except FairTraceException:
        # Re-raise domain exceptions (401 AuthenticationFailedError) — handled by app-level handler
        raise
    except Exception:
        tb = traceback.format_exc()
        logger.error(
            "login_authenticate_error",
            email=body.email,
            traceback=tb,
            request_id=request_id,
            exc_info=True,
        )
        raise

    try:
        audit_repo.create(db, {
            "event_type": AuditEventType.USER_LOGIN,
            "actor_id": user.id,
            "actor_role": user.role,
            "resource_type": "user",
            "resource_id": user.id,
            "event_payload": {"email": user.email},
            "ip_address": ip,
            "correlation_id": request_id,
        })
        db.commit()
    except Exception:
        tb = traceback.format_exc()
        logger.error(
            "login_audit_error",
            email=body.email,
            traceback=tb,
            request_id=request_id,
            exc_info=True,
        )
        # Audit failure must NOT block login — rollback the audit only, not the session
        db.rollback()

    try:
        token_response = create_token_for_user(user)
        logger.info(
            "login_success",
            email=user.email,
            role=user.role.value,
            user_id=str(user.id),
            request_id=request_id,
        )
        return token_response
    except Exception:
        tb = traceback.format_exc()
        logger.error(
            "login_token_creation_error",
            email=body.email,
            traceback=tb,
            request_id=request_id,
            exc_info=True,
        )
        raise
