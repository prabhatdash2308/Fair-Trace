import { Navigate } from 'react-router-dom';
import { useAuthStore } from '@/store';
import { ROLE_HIERARCHY } from '@/constants/roles';
import { ROUTES } from '@/constants/routes';
import type { Role } from '@/constants/roles';
import type { ReactNode } from 'react';

interface RoleGuardProps {
  /** Minimum role required to access this route/component. */
  requiredRole: Role;
  children: ReactNode;
  /** Optional: render a custom fallback instead of redirecting. */
  fallback?: ReactNode;
}

/**
 * RoleGuard — renders children only if the current user has sufficient role.
 * Uses role hierarchy: ADMIN > MANAGER > EMPLOYEE.
 */
export function RoleGuard({ requiredRole, children, fallback }: RoleGuardProps) {
  const { user } = useAuthStore();

  if (!user) {
    return <Navigate to={ROUTES.LOGIN} replace />;
  }

  const userLevel = ROLE_HIERARCHY[user.role as Role] ?? 0;
  const requiredLevel = ROLE_HIERARCHY[requiredRole] ?? 0;

  if (userLevel < requiredLevel) {
    if (fallback) return <>{fallback}</>;
    return <Navigate to={ROUTES.DASHBOARD} replace />;
  }

  return <>{children}</>;
}
