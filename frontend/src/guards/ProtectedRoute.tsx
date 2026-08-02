import { Navigate, useLocation } from 'react-router-dom';
import { useAuthStore } from '@/store/auth/auth.store';
import { ROUTES } from '@/constants/routes';
import { DEMO_MODE } from '@/config/demo';
import type { ReactNode } from 'react';

interface ProtectedRouteProps {
  children: ReactNode;
}

/**
 * ProtectedRoute — redirects unauthenticated users to /login.
 * In DEMO_MODE, always allows access without any auth check.
 */
export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isAuthenticated } = useAuthStore();
  const location = useLocation();

  // DEMO MODE: bypass all auth checks
  if (DEMO_MODE) return <>{children}</>;

  if (!isAuthenticated) {
    return <Navigate to={ROUTES.LOGIN} state={{ from: location }} replace />;
  }

  return <>{children}</>;
}
