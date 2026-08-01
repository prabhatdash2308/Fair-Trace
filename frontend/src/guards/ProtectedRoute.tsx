import { Navigate, useLocation } from 'react-router-dom';
import { useAuthStore } from '@/store';
import { ROUTES } from '@/constants/routes';
import type { ReactNode } from 'react';

interface ProtectedRouteProps {
  children: ReactNode;
}

/**
 * ProtectedRoute — redirects unauthenticated users to /login.
 * Preserves the attempted path so we can redirect back after login.
 */
export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isAuthenticated } = useAuthStore();
  const location = useLocation();

  if (!isAuthenticated) {
    return <Navigate to={ROUTES.LOGIN} state={{ from: location }} replace />;
  }

  return <>{children}</>;
}
