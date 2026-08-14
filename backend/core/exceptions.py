"""
FairTrace — Custom Exception Hierarchy
All domain exceptions inherit from FairTraceException.
Routers catch these and convert them to HTTP responses via exception handlers.
"""


class FairTraceException(Exception):
    """Base exception for all FairTrace domain errors."""

    error_code: str = "INTERNAL_ERROR"
    http_status: int = 500
    message: str = "An unexpected error occurred."

    def __init__(self, message: str | None = None):
        self.message = message or self.__class__.message
        super().__init__(self.message)


# ── Authentication & Authorization ─────────────────────────────────────────────

class InvalidTokenError(FairTraceException):
    error_code = "INVALID_TOKEN"
    http_status = 401
    message = "Authentication required. Token is missing or invalid."


class AuthenticationFailedError(FairTraceException):
    error_code = "AUTHENTICATION_FAILED"
    http_status = 401
    message = "Invalid email or password."


class ForbiddenError(FairTraceException):
    error_code = "FORBIDDEN"
    http_status = 403
    message = "You do not have permission to perform this action."


# ── Resource Errors ────────────────────────────────────────────────────────────

class NotFoundError(FairTraceException):
    error_code = "NOT_FOUND"
    http_status = 404
    message = "The requested resource was not found."


class ConflictError(FairTraceException):
    error_code = "CONFLICT"
    http_status = 409
    message = "A conflict occurred with the current state of the resource."


# ── Business Rule Errors ───────────────────────────────────────────────────────

class InvalidStateError(FairTraceException):
    error_code = "INVALID_STATE"
    http_status = 409
    message = "The resource is not in a valid state for this action."


class BusinessValidationError(FairTraceException):
    error_code = "VALIDATION_ERROR"
    http_status = 400
    message = "The request did not meet business rule requirements."


class InsufficientEvidenceError(FairTraceException):
    error_code = "INSUFFICIENT_EVIDENCE"
    http_status = 422
    message = "Insufficient evidence to generate a reliable report."


# ── Pipeline & Agent Errors ────────────────────────────────────────────────────

class PipelineError(FairTraceException):
    error_code = "PIPELINE_ERROR"
    http_status = 500
    message = "The AI pipeline encountered an error."


class ModelUnavailableError(FairTraceException):
    error_code = "MODEL_UNAVAILABLE"
    http_status = 503
    message = "The AI model is temporarily unavailable. Please retry in 30–60 seconds."


class CircuitOpenError(FairTraceException):
    error_code = "CIRCUIT_OPEN"
    http_status = 503
    message = "AI service temporarily unavailable due to repeated failures. Please retry."


class PromptValidationError(FairTraceException):
    error_code = "PROMPT_VALIDATION_ERROR"
    http_status = 500
    message = "The AI model returned an unexpected response format."
