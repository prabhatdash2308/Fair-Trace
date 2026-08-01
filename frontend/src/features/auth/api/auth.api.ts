import apiClient from '@/api/client';
import { API_ENDPOINTS } from '@/constants/api';
import type { LoginRequest, LoginResponse, AuthUser } from '../types/auth.types';

/**
 * Auth feature API module.
 * Uses the shared apiClient from Phase 1 — no duplicate instances.
 * All interceptors (auth, retry, error) are already applied.
 */
export const authFeatureApi = {
  /**
   * POST /auth/login
   * Returns access_token, optional refresh_token, and user profile.
   */
  login: (credentials: LoginRequest) =>
    apiClient
      .post<LoginResponse>(API_ENDPOINTS.AUTH.LOGIN, credentials)
      .then((r) => r.data),

  /**
   * POST /auth/logout
   * Server-side token invalidation (best-effort — we always clear locally).
   */
  logout: () =>
    apiClient
      .post(API_ENDPOINTS.AUTH.LOGOUT)
      .then((r) => r.data)
      .catch(() => {
        // Logout must always succeed locally even if server is unreachable
      }),

  /**
   * GET /auth/me
   * Fetches the current user from the server — used for session hydration.
   */
  me: () =>
    apiClient
      .get<AuthUser>(API_ENDPOINTS.AUTH.ME)
      .then((r) => r.data),
};
