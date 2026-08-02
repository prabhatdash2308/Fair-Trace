import type { AxiosInstance } from 'axios';
import type { ApiError } from '@/types';
import { DEMO_MODE } from '@/config/demo';
import { getDemoDataForUrl } from './mock.data';

/**
 * Error interceptor — normalises all API errors into a consistent ApiError shape.
 * Consumers can always rely on error.message and error.status.
 */
export function applyErrorInterceptor(client: AxiosInstance): void {
  client.interceptors.response.use(
    (response) => response,
    (error: unknown) => {
      const axiosError = error as {
        response?: { status?: number; data?: { detail?: string; message?: string; error?: string } };
        message?: string;
        code?: string;
      };

      const status = axiosError.response?.status ?? 0;
      const data = axiosError.response?.data;
      const url = (error as { config?: { url?: string } })?.config?.url ?? '';

      let errorMessage = 'An unexpected error occurred. Please try again or contact support.';
      
      // 1. If it's a 401, we want a clean auth message
      if (status === 401) {
        errorMessage = 'Your session has expired or is invalid. Please sign in again.';
      }
      // 2. If it's an Auth Endpoint error (400, 403, 500)
      else if (url.includes('/auth/login') || url.includes('/auth')) {
        errorMessage = 'Unable to sign in. Please verify your credentials or contact your administrator.';
      }
      // 3. Known clean validation errors (422)
      else if (status === 422) {
        errorMessage = 'Please check the information you entered and try again.';
      }
      // 4. Client Errors (400-499) that aren't 401
      else if (status >= 400 && status < 500) {
        // Only use backend messages if they are simple strings and not tracebacks
        const rawMessage = data?.message ?? data?.detail ?? data?.error;
        if (typeof rawMessage === 'string' && rawMessage.length < 100 && !rawMessage.includes('Traceback')) {
          errorMessage = rawMessage;
        } else {
          errorMessage = 'The request could not be completed. Please try again.';
        }
      }
      // 5. Server Errors (500+) must always be masked in production
      else if (status >= 500) {
        errorMessage = 'The server encountered an issue. Please contact your administrator.';
      }

      // Log real technical details to console ONLY in development
      if (import.meta.env.DEV) {
        console.error('[API Error]:', { status, url, data, rawError: error });
      }

      // DEMO MODE: Never throw runtime exceptions for API failures.
      // Intercept the error and return realistic mock data.
      if (DEMO_MODE) {
        const method = (error as { config?: { method?: string } })?.config?.method?.toLowerCase() || 'get';
        const mockData = getDemoDataForUrl(url, method);
        console.warn(`[DEMO MODE] API Failed (${status}) for ${method.toUpperCase()} ${url}. Returning mock data.`);
        // Resolve the promise to simulate a successful API response
        return Promise.resolve({ data: mockData, status: 200, statusText: 'OK', headers: {}, config: (error as any).config });
      }

      const normalised: ApiError = {
        status,
        message: errorMessage,
        code: axiosError.code,
        details: import.meta.env.DEV ? (data as Record<string, unknown> | undefined) : undefined,
      };

      return Promise.reject(normalised);
    }
  );
}

