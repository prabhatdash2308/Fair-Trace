import type { AxiosInstance } from 'axios';
import { useAuthStore } from '@/store/auth/auth.store';
import { DEMO_MODE, DEMO_TOKEN } from '@/config/demo';

/**
 * Auth interceptor — injects the Bearer token on every request.
 * On 401 response, clears storage and redirects to login.
 *
 * In DEMO_MODE: injects the demo token and NEVER redirects on 401
 * so backend auth errors don't break the demo flow.
 */
export function applyAuthInterceptor(client: AxiosInstance): void {
  // Request: inject token from Zustand (or demo token)
  client.interceptors.request.use((config) => {
    const token = DEMO_MODE ? DEMO_TOKEN : useAuthStore.getState().token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  });

  // Response: handle 401 — skip entirely in demo mode
  client.interceptors.response.use(
    (response) => response,
    (error: unknown) => {
      const status = (error as { response?: { status?: number } })?.response?.status;
      if (!DEMO_MODE && status === 401) {
        useAuthStore.getState().logout();
        localStorage.removeItem('rg_token');
        localStorage.removeItem('rg_refresh_token');
        localStorage.removeItem('rg_remember');
        localStorage.removeItem('rg_user');
        window.location.href = '/login';
      }
      return Promise.reject(error);
    }
  );
}
