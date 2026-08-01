import type { UserRole } from '@/types';

/**
 * Auth feature-specific types.
 * Isolated here so the global api.types.ts stays domain-focused.
 */

export interface AuthUser {
  id: string;
  email: string;
  full_name: string;
  role: UserRole;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token?: string;
  token_type: string;
  user: AuthUser;
}

export interface AuthSession {
  accessToken: string;
  refreshToken: string | null;
  user: AuthUser;
  isAuthenticated: boolean;
  expiresAt: number | null; // Unix ms timestamp
}

export interface LoginFormValues {
  email: string;
  password: string;
  rememberMe: boolean;
}
