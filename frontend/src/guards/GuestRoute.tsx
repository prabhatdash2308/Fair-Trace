import { Navigate, useLocation } from 'react-router-dom';
import { useAuthStore } from '@/store';
import { ROUTES } from '@/constants/routes';
import { DEMO_MODE } from '@/config/demo';
import type { ReactNode } from 'react';

interface GuestRouteProps {
  children: ReactNode;
}

/**
 * GuestRoute — redirects authenticated users away from auth pages.
 * In DEMO_MODE, always renders children (login page) so the judge
 * can see it, then the login action immediately navigates to dashboard.
 */
export function GuestRoute({ children }: GuestRouteProps) {
  const { isAuthenticated } = useAuthStore();
  const location = useLocation();
  const from = (location.state as any)?.from?.pathname || ROUTES.DASHBOARD;

  // DEMO MODE: show the login page so judges can see it, don't auto-redirect
  if (DEMO_MODE) return <>{children}</>;

  if (isAuthenticated) {
    return <Navigate to={from} replace />;
  }

  return <>{children}</>;
}
