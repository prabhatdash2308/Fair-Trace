import { Navigate, useLocation } from 'react-router-dom';
import { useAuthStore } from '@/store/auth/auth.store';
import { ROUTES } from '@/constants/routes';
import { isTokenExpired } from '@/features/auth/utils/auth.utils';
import type { ReactNode } from 'react';

interface ProtectedRouteProps {
  children: ReactNode;
}

/**
 * ProtectedRoute — redirects unauthenticated or expired-session users to /login.
 * Preserves the attempted path in location state for post-login redirect.
 */
export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isAuthenticated, token } = useAuthStore();
  const location = useLocation();

  // Check both auth flag and token expiry
  const isValid = isAuthenticated && !isTokenExpired(token);

  if (!isValid) {
    return <Navigate to={ROUTES.LOGIN} state={{ from: location }} replace />;
  }

  return <>{children}</>;
}
