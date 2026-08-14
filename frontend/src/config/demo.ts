/**
 * FairTrace — Demo Mode Configuration
 *
 * Set VITE_DEMO_MODE=true in your .env to enable demo mode.
 * Production deployments must set VITE_DEMO_MODE=false or omit the variable.
 *
 * When enabled:
 * - Login always succeeds instantly (no API call)
 * - All protected routes allow access
 * - A synthetic admin user is injected into the auth store
 * - JWT tokens are never required
 */

export const DEMO_MODE = import.meta.env.VITE_DEMO_MODE === 'true';

export const DEMO_USER = {
  id: '00000000-0000-0000-0000-000000000001',
  email: 'admin@fairtrace.ai',
  full_name: 'Admin User',
  role: 'ADMIN' as const,
};

export const DEMO_TOKEN = 'demo-mode-token-fairtrace-2026';
