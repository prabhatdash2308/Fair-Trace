"""ReviewGuard AI — Structured Request/Response Logging Middleware"""

import time

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = structlog.get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Logs every request and response as structured JSON.
    Excludes: Authorization header values, /health endpoint (to reduce noise).
    Includes: method, path, status_code, duration_ms, correlation_id.
    """

    _SKIP_PATHS = {"/health", "/docs", "/redoc", "/openapi.json"}

    async def dispatch(self, request: Request, call_next) -> Response:
        if request.url.path in self._SKIP_PATHS:
            return await call_next(request)

        start = time.time()
        correlation_id = getattr(request.state, "correlation_id", "")

        logger.info(
            "request_received",
            method=request.method,
            path=request.url.path,
            correlation_id=correlation_id,
            ip_address=request.client.host if request.client else None,
        )

        response = await call_next(request)
        duration_ms = int((time.time() - start) * 1000)

        logger.info(
            "response_sent",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=duration_ms,
            correlation_id=correlation_id,
        )

        return response
