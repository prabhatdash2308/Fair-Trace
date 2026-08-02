import type { AxiosInstance } from 'axios';

import { useAuthStore } from '@/store/auth/auth.store';

/**
 * Auth interceptor — injects the Bearer token on every request.
 * On 401 response, clears storage and redirects to login.
 */
export function applyAuthInterceptor(client: AxiosInstance): void {
  // Request: inject token from Zustand
  client.interceptors.request.use((config) => {
    const token = useAuthStore.getState().token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  });

  // Response: handle 401
  client.interceptors.response.use(
    (response) => response,
    (error: unknown) => {
      const status = (error as { response?: { status?: number } })?.response?.status;
      if (status === 401) {
        // Use the auth store's logout to ensure synchronous state update
        useAuthStore.getState().logout();
        
        // Also clear any legacy manual tokens just in case
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
