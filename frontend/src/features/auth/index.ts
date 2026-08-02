/**
 * Auth feature public API.
 * Import from '@/features/auth' — never reach into internal modules directly.
 */

// Components
export { LoginCard } from './components/LoginCard';
export { LoginForm } from './components/LoginForm';
export { PasswordField } from './components/PasswordField';
export { RememberMe } from './components/RememberMe';
export { RoleSelector } from './components/RoleSelector';
export { DemoCredentials } from './components/DemoCredentials';

// Hooks
export { useLogin } from './hooks/useLogin';

// Service
export { authService } from './services/auth.service';

// Schema
export { loginSchema } from './schemas/login.schema';
export type { LoginSchema } from './schemas/login.schema';

// Types
export type { AuthUser, LoginRequest, LoginResponse, AuthSession, LoginFormValues } from './types/auth.types';

// Utils
export { clearTokens, getStoredToken, isTokenExpired } from './utils/auth.utils';
