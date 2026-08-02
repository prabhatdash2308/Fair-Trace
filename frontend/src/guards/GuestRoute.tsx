import { Navigate, useLocation } from 'react-router-dom';
import { useAuthStore } from '@/store';
import { ROUTES } from '@/constants/routes';
import type { ReactNode } from 'react';

interface GuestRouteProps {
  children: ReactNode;
}

/**
 * GuestRoute — redirects authenticated users away from auth pages (login, register).
 * Prevents logged-in users from seeing the login form.
 */
export function GuestRoute({ children }: GuestRouteProps) {
  const { isAuthenticated } = useAuthStore();

  const location = useLocation();
  const from = (location.state as any)?.from?.pathname || ROUTES.DASHBOARD;

  if (isAuthenticated) {
    return <Navigate to={from} replace />;
  }

  return <>{children}</>;
}
