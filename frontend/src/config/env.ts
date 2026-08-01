/**
 * Environment configuration.
 * Single source of truth for all env variables.
 * Never use import.meta.env directly outside this file.
 */
export const env = {
  apiBaseUrl: (import.meta.env.VITE_API_BASE_URL as string) ?? '/api/v1',
  appVersion: (import.meta.env.VITE_APP_VERSION as string) ?? '1.0.0',
  appEnv: (import.meta.env.VITE_APP_ENV as 'development' | 'staging' | 'production') ?? 'development',
  isDevelopment: import.meta.env.DEV,
  isProduction: import.meta.env.PROD,
} as const;
