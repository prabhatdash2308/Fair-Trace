"""ReviewGuard AI — Correlation ID Middleware
Reads or generates X-Correlation-Id and attaches to request state and response headers.
"""

import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class CorrelationMiddleware(BaseHTTPMiddleware):
    """
    Reads X-Correlation-Id from incoming request.
    If absent, generates a new UUID.
    Attaches to request.state.correlation_id for downstream use.
    Echoes in response header.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        correlation_id = request.headers.get("X-Correlation-Id") or str(uuid.uuid4())
        request.state.correlation_id = correlation_id
        response = await call_next(request)
        response.headers["X-Correlation-Id"] = correlation_id
        return response
