"""
ReviewGuard AI — FastAPI Application Entry Point
All middleware, routers, exception handlers, and startup checks are registered here.
No business logic lives in this file.
"""

import structlog
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from config import settings
from core.exceptions import ReviewGuardException
from app.ai.services.qdrant_service import ensure_collection, health_check as qdrant_health
from middleware.correlation_middleware import CorrelationMiddleware
from middleware.logging_middleware import LoggingMiddleware
from routers.routers import (
    users_router,
    cycles_router,
    inputs_router,
    pipeline_router,
    reports_router,
    audit_router,
)
from routers.auth import router as auth_router

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.JSONRenderer(),
    ]
)

logger = structlog.get_logger(__name__)

# ── App Instance ───────────────────────────────────────────────────────────────

app = FastAPI(
    title="ReviewGuard AI API",
    version=settings.app_version,
    description=(
        "**Evidence-Grounded, Bias-Aware Multi-Agent Performance Review Intelligence**\n\n"
        "Architectural Principles:\n"
        "- **P1** Evidence Before Intelligence\n"
        "- **P3** Human Owns Decisions\n"
        "- **P4** Fail Safe — refuse rather than hallucinate\n\n"
        "All endpoints require `Authorization: Bearer <jwt>` except `/health` and `/api/v1/auth/login`."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={"name": "ReviewGuard AI Team", "email": "team@reviewguard.ai"},
    license_info={"name": "MIT"},
)

# ── Middleware (registered bottom-up — applied top-down) ──────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Correlation-Id"],
)
app.add_middleware(LoggingMiddleware)
app.add_middleware(CorrelationMiddleware)

# ── Exception Handlers ─────────────────────────────────────────────────────────

@app.exception_handler(ReviewGuardException)
async def review_guard_exception_handler(request: Request, exc: ReviewGuardException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.http_status,
        content={
            "error": exc.error_code,
            "message": exc.message,
            "detail": str(exc) if settings.is_development else None,
            "request_id": getattr(request.state, "correlation_id", None),
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "error": "VALIDATION_ERROR",
            "message": "Request validation failed. Check the 'detail' field for field-level errors.",
            "detail": exc.errors(),
            "request_id": getattr(request.state, "correlation_id", None),
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("unhandled_exception", error=str(exc))
    return JSONResponse(
        status_code=500,
        content={
            "error": "INTERNAL_ERROR",
            "message": "An unexpected error occurred.",
            "detail": str(exc) if settings.is_development else None,
            "request_id": getattr(request.state, "correlation_id", None),
        },
    )


# ── Routers ────────────────────────────────────────────────────────────────────

API_V1 = "/api/v1"

app.include_router(auth_router,     prefix=f"{API_V1}/auth",          tags=["Authentication"])
app.include_router(users_router,    prefix=f"{API_V1}/users",          tags=["Users"])
app.include_router(cycles_router,   prefix=f"{API_V1}/review-cycles",  tags=["Review Cycles"])
app.include_router(inputs_router,   prefix=f"{API_V1}/review-cycles",  tags=["Inputs"])
app.include_router(pipeline_router, prefix=f"{API_V1}",                tags=["Pipeline"])
app.include_router(reports_router,  prefix=f"{API_V1}/reports",        tags=["Reports"])
app.include_router(audit_router,    prefix=f"{API_V1}/audit",          tags=["Audit"])


# ── Health Check ───────────────────────────────────────────────────────────────

@app.get(
    "/health",
    summary="Health Check",
    description="Returns system health for all services. No authentication required.",
    tags=["System"],
)
async def health_check():
    from core.database import engine
    db_healthy = False
    try:
        with engine.connect() as conn:
            conn.execute(__import__("sqlalchemy").text("SELECT 1"))
        db_healthy = True
    except Exception:
        pass

    qdrant_ok = qdrant_health()

    all_healthy = db_healthy and qdrant_ok
    return JSONResponse(
        status_code=200 if all_healthy else 503,
        content={
            "status": "healthy" if all_healthy else "degraded",
            "version": settings.app_version,
            "environment": settings.environment,
            "services": {
                "database": db_healthy,
                "vector_store": qdrant_ok,
            },
        },
    )


# ── Startup / Shutdown ─────────────────────────────────────────────────────────

@app.on_event("startup")
async def startup() -> None:
    logger.info("reviewguard_api_starting", version=settings.app_version, env=settings.environment)

    # Ensure Qdrant collection exists
    try:
        ensure_collection()
        logger.info("qdrant_collection_ready", collection=settings.qdrant_collection_name)
    except Exception as exc:
        logger.error("qdrant_startup_failed", error=str(exc))

    # Run Alembic migrations automatically in development
    if settings.is_development:
        try:
            from alembic.config import Config
            from alembic import command
            alembic_cfg = Config("alembic.ini")
            command.upgrade(alembic_cfg, "head")
            logger.info("alembic_migrations_applied")
        except Exception as exc:
            logger.warning("alembic_migration_warning", error=str(exc))

    logger.info("reviewguard_api_ready", docs_url="/docs")


@app.on_event("shutdown")
async def shutdown() -> None:
    logger.info("reviewguard_api_shutting_down")
