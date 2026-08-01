import type { AxiosInstance } from 'axios';

const TOKEN_KEY = 'rg_token';

/**
 * Auth interceptor — injects the Bearer token on every request.
 * On 401 response, clears storage and redirects to login.
 */
export function applyAuthInterceptor(client: AxiosInstance): void {
  // Request: inject token
  client.interceptors.request.use((config) => {
    const token = localStorage.getItem(TOKEN_KEY);
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
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem('rg_user');
        window.location.href = '/login';
      }
      return Promise.reject(error);
    }
  );
}
