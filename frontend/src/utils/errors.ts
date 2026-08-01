import type { ApiError } from '@/types';

/**
 * HTTP status code → user-facing message map.
 * Keep copy-writing consistent across all feature modules.
 */
const HTTP_MESSAGES: Record<number, string> = {
  400: 'Invalid request. Please check your input and try again.',
  401: 'Your session has expired. Please sign in again.',
  403: 'You do not have permission to perform this action.',
  404: 'The requested resource was not found.',
  409: 'This action conflicts with the current state. Please refresh and try again.',
  422: 'Validation failed. Please check your input.',
  429: 'Too many requests. Please wait a moment and try again.',
  500: 'A server error occurred. Our team has been notified.',
  502: 'Service temporarily unavailable. Please try again shortly.',
  503: 'Service temporarily unavailable. Please try again shortly.',
};

/** Returns a descriptive message for the given HTTP status code. */
export function getHttpErrorMessage(status: number): string {
  return HTTP_MESSAGES[status] ?? `An unexpected error occurred (HTTP ${status}).`;
}

/** Type-narrow to check whether a thrown value is an ApiError. */
export function isApiError(error: unknown): error is ApiError {
  return (
    typeof error === 'object' &&
    error !== null &&
    'status' in error &&
    'message' in error
  );
}

/**
 * Extracts the first validation error detail from a FastAPI 422 response.
 * FastAPI returns: { detail: [{ loc: [...], msg: "...", type: "..." }] }
 */
export function extractValidationError(error: ApiError): string {
  const detail = error.details?.['detail'];
  if (Array.isArray(detail) && detail.length > 0) {
    const first = detail[0] as { loc?: string[]; msg?: string };
    const field = first.loc?.slice(-1)[0] ?? 'field';
    return `${field}: ${first.msg ?? 'Invalid value'}`;
  }
  return error.message;
}

/**
 * Returns a user-facing error message from any thrown value.
 * Safe to call in onError callbacks without type checks.
 */
export function getErrorMessage(error: unknown): string {
  if (isApiError(error)) {
    if (error.status === 422) return extractValidationError(error);
    return error.message || getHttpErrorMessage(error.status);
  }
  if (error instanceof Error) return error.message;
  return 'An unexpected error occurred.';
}
