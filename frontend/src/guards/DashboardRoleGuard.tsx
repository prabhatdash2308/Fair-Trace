import { Navigate } from 'react-router-dom';
import { useAuthStore } from '@/store/auth/auth.store';
import { ROUTES } from '@/constants/routes';
import { DEMO_MODE } from '@/config/demo';
import type { ReactNode } from 'react';
import type { Role } from '@/constants/roles';

interface DashboardRoleGuardProps {
  requiredRole: Role;
  children: ReactNode;
}

/**
 * DashboardRoleGuard — enforces strict exact-role access to role dashboards.
 * In DEMO_MODE, always grants access (demo user is ADMIN, sees all).
 */
export function DashboardRoleGuard({ requiredRole, children }: DashboardRoleGuardProps) {
  const { user, isAuthenticated } = useAuthStore();

  // DEMO MODE: bypass role check entirely — admin sees everything
  if (DEMO_MODE) return <>{children}</>;

  if (!isAuthenticated || !user) {
    return <Navigate to={ROUTES.LOGIN} replace />;
  }

  if (user.role !== requiredRole) {
    return <Navigate to={ROUTES.UNAUTHORIZED} replace />;
  }

  return <>{children}</>;
}
