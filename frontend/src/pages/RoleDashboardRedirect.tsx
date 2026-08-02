import { Navigate } from 'react-router-dom';
import { useAuthStore } from '@/store/auth/auth.store';
import { roleDashboardRoute } from '@/constants/routes';

/**
 * RoleDashboardRedirect — reads the current user's role and immediately
 * redirects to the correct role-specific dashboard.
 *
 * Used at /dashboard so old bookmarks and external links still work.
 */
export function RoleDashboardRedirect() {
  const { user } = useAuthStore();
  const target = roleDashboardRoute(user?.role);
  return <Navigate to={target} replace />;
}
