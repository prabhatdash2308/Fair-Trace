/**
 * ReviewGuard AI — Demo Mode Configuration
 *
 * HACKATHON DEMO MODE — Set DEMO_MODE = true to bypass all authentication.
 * To restore production auth, set DEMO_MODE = false.
 *
 * When enabled:
 * - Login always succeeds instantly (no API call)
 * - All protected routes allow access
 * - A synthetic admin user is injected into the auth store
 * - JWT tokens are never required
 */

export const DEMO_MODE = true;

export const DEMO_USER = {
  id: '00000000-0000-0000-0000-000000000001',
  email: 'admin@reviewguard.ai',
  full_name: 'Admin User',
  role: 'ADMIN' as const,
};

export const DEMO_TOKEN = 'demo-mode-token-hackathon-2026';
