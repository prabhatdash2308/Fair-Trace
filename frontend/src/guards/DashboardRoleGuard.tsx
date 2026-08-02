import { Navigate } from 'react-router-dom';
import { useAuthStore } from '@/store/auth/auth.store';
import { ROUTES } from '@/constants/routes';
import type { ReactNode } from 'react';
import type { Role } from '@/constants/roles';

interface DashboardRoleGuardProps {
  /** The exact role required to access this dashboard. */
  requiredRole: Role;
  children: ReactNode;
}

/**
 * DashboardRoleGuard — enforces strict exact-role access to role-specific dashboards.
 *
 * Unlike RoleGuard (which uses hierarchy), this guard enforces an exact match.
 * A MANAGER cannot access /dashboard/admin even though ADMIN > MANAGER.
 *
 * If the user has a different role → renders the UnauthorizedPage.
 * If the user is unauthenticated → redirects to /login.
 */
export function DashboardRoleGuard({ requiredRole, children }: DashboardRoleGuardProps) {
  const { user, isAuthenticated } = useAuthStore();

  if (!isAuthenticated || !user) {
    return <Navigate to={ROUTES.LOGIN} replace />;
  }

  if (user.role !== requiredRole) {
    return <Navigate to={ROUTES.UNAUTHORIZED} replace />;
  }

  return <>{children}</>;
}
