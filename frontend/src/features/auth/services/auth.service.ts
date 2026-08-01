import { useAuthStore } from '@/store/auth/auth.store';
import { queryClient } from '@/app/providers/QueryProvider';
import { authFeatureApi } from '../api/auth.api';
import {
  persistTokens,
  clearTokens,
  setRememberMe,
  getTokenExpiry,
} from '../utils/auth.utils';
import type { LoginRequest, LoginResponse } from '../types/auth.types';

/**
 * Auth service — orchestrates the full auth lifecycle.
 *
 * Responsibilities:
 *  - Call the API
 *  - Update Zustand store
 *  - Persist tokens to localStorage
 *  - Invalidate / clear React Query cache
 *
 * Components and hooks call this service, not the API directly.
 */
export const authService = {
  /**
   * Executes the full login sequence.
   * Persists tokens and hydrates the auth store.
   */
  async login(credentials: LoginRequest, rememberMe = false): Promise<LoginResponse> {
    const response = await authFeatureApi.login(credentials);

    const { access_token, refresh_token, user } = response;

    // Persist to localStorage
    persistTokens(access_token, refresh_token);
    setRememberMe(rememberMe);

    // Hydrate Zustand store
    const store = useAuthStore.getState();
    store.login(access_token, {
      id: user.id,
      email: user.email,
      full_name: user.full_name,
      role: user.role,
    });

    // Also store refresh token and expiry in the auth store
    const expiresAt = getTokenExpiry(access_token);
    useAuthStore.setState({
      refreshToken: refresh_token ?? null,
      expiresAt,
    });

    return response;
  },

  /**
   * Full logout — clears everything.
   * Server logout is best-effort.
   */
  async logout(): Promise<void> {
    // Best-effort server logout
    await authFeatureApi.logout();

    // Clear tokens from storage
    clearTokens();

    // Clear Zustand store
    useAuthStore.getState().logout();

    // Clear all React Query cache
    queryClient.clear();
  },
};
