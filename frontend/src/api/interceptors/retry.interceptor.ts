import type { AxiosInstance, InternalAxiosRequestConfig } from 'axios';

interface RetryConfig extends InternalAxiosRequestConfig {
  _retryCount?: number;
  _maxRetries?: number;
}

const DEFAULT_MAX_RETRIES = 2;
const RETRY_DELAY_MS = 1000;

// Status codes that should NOT be retried
const NON_RETRYABLE = new Set([400, 401, 403, 404, 409, 422]);

/**
 * Retry interceptor — automatically retries idempotent requests on transient failures.
 * Does NOT retry on auth errors or client errors.
 */
export function applyRetryInterceptor(client: AxiosInstance): void {
  client.interceptors.response.use(
    (response) => response,
    async (error: unknown) => {
      const axiosError = error as {
        config?: RetryConfig;
        response?: { status?: number };
        code?: string;
      };

      const config = axiosError.config;
      if (!config) return Promise.reject(error);

      const status = axiosError.response?.status;
      const isNetworkError = !axiosError.response && axiosError.code !== 'ECONNABORTED';

      // Don't retry non-retryable status codes
      if (status && NON_RETRYABLE.has(status)) {
        return Promise.reject(error);
      }

      // Don't retry POST/DELETE by default (not idempotent)
      const method = (config.method ?? '').toUpperCase();
      if (method === 'POST' || method === 'DELETE') {
        return Promise.reject(error);
      }

      config._retryCount = (config._retryCount ?? 0) + 1;
      const maxRetries = config._maxRetries ?? DEFAULT_MAX_RETRIES;

      if (config._retryCount > maxRetries) {
        return Promise.reject(error);
      }

      // Only retry on 5xx or network errors
      if (!isNetworkError && (!status || status < 500)) {
        return Promise.reject(error);
      }

      // Exponential backoff
      const delay = RETRY_DELAY_MS * 2 ** (config._retryCount - 1);
      await new Promise((resolve) => setTimeout(resolve, delay));

      return client(config);
    }
  );
}
