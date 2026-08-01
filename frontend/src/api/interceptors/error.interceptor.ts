import type { AxiosInstance } from 'axios';
import type { ApiError } from '@/types';

/**
 * Error interceptor — normalises all API errors into a consistent ApiError shape.
 * Consumers can always rely on error.message and error.status.
 */
export function applyErrorInterceptor(client: AxiosInstance): void {
  client.interceptors.response.use(
    (response) => response,
    (error: unknown) => {
      const axiosError = error as {
        response?: { status?: number; data?: { detail?: string; message?: string } };
        message?: string;
        code?: string;
      };

      const status = axiosError.response?.status ?? 0;
      const data = axiosError.response?.data;

      const normalised: ApiError = {
        status,
        message:
          data?.detail ??
          data?.message ??
          axiosError.message ??
          'An unexpected error occurred.',
        code: axiosError.code,
        details: data as Record<string, unknown> | undefined,
      };

      return Promise.reject(normalised);
    }
  );
}
