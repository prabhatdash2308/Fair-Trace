/**
 * Auth utilities — pure functions, no side effects.
 * Keeps logic testable and out of components/hooks.
 */

const TOKEN_KEY = 'rg_token';
const REFRESH_KEY = 'rg_refresh_token';
const REMEMBER_KEY = 'rg_remember';

/** Persist tokens to localStorage (used when Remember Me is checked). */
export function persistTokens(accessToken: string, refreshToken?: string | null): void {
  localStorage.setItem(TOKEN_KEY, accessToken);
  if (refreshToken) localStorage.setItem(REFRESH_KEY, refreshToken);
}

/** Remove all auth tokens from storage. */
export function clearTokens(): void {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(REFRESH_KEY);
  localStorage.removeItem(REMEMBER_KEY);
}

/** Read the stored access token. */
export function getStoredToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

/** Read the stored refresh token. */
export function getStoredRefreshToken(): string | null {
  return localStorage.getItem(REFRESH_KEY);
}

/** Set the Remember Me preference. */
export function setRememberMe(value: boolean): void {
  if (value) {
    localStorage.setItem(REMEMBER_KEY, '1');
  } else {
    localStorage.removeItem(REMEMBER_KEY);
  }
}

/** Check if Remember Me was previously set. */
export function getRememberMe(): boolean {
  return localStorage.getItem(REMEMBER_KEY) === '1';
}

/**
 * Decode the expiry time from a JWT access token.
 * Returns a Unix ms timestamp, or null if the token is malformed.
 */
export function getTokenExpiry(token: string): number | null {
  try {
    const parts = token.split('.');
    if (parts.length !== 3) return null;
    const payload = JSON.parse(atob(parts[1]));
    return typeof payload.exp === 'number' ? payload.exp * 1000 : null;
  } catch {
    return null;
  }
}

/** Returns true if the token is expired (or expiry is unknown). */
export function isTokenExpired(token: string | null): boolean {
  if (!token) return true;
  const expiry = getTokenExpiry(token);
  if (!expiry) return false; // Unknown expiry — assume valid
  return Date.now() > expiry;
}
