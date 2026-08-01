import { Navigate } from 'react-router-dom';
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

  if (isAuthenticated) {
    return <Navigate to={ROUTES.DASHBOARD} replace />;
  }

  return <>{children}</>;
}
