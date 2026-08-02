import { useMutation } from '@tanstack/react-query';
import { useNavigate, useLocation } from 'react-router-dom';
import { authService } from '../services/auth.service';
import { roleDashboardRoute } from '@/constants/routes';
import type { LoginSchema } from '../schemas/login.schema';
import type { ApiError } from '@/types';

/**
 * useLogin — TanStack Query mutation hook for the login flow.
 *
 * Responsibilities (in order):
 *  1. Call authService.login (handles API + store + persistence)
 *  2. Read the user's role from the login response
 *  3. Redirect to the role-specific dashboard:
 *       ADMIN    → /dashboard/admin
 *       MANAGER  → /dashboard/manager
 *       EMPLOYEE → /dashboard/employee
 *  4. Respects the `from` location if the user was redirected from a known route.
 *  5. Surface API errors to the calling component via mutation.error
 */
export function useLogin() {
  const navigate = useNavigate();
  const location = useLocation();

  // If the user was redirected from a specific route, honor it
  // (e.g., /dashboard/manager bookmark → redirected to /login → should go back to /dashboard/manager after login)
  const from =
    (location.state as { from?: { pathname: string } })?.from?.pathname ?? null;

  const mutation = useMutation({
    mutationFn: ({ email, password, rememberMe }: LoginSchema) =>
      authService.login({ email, password }, rememberMe),

    onSuccess: (response) => {
      // Determine redirect: honor original destination, otherwise use role dashboard
      const roleTarget = roleDashboardRoute(response.user.role);
      const destination = from ?? roleTarget;
      navigate(destination, { replace: true });
    },

    // onError is handled by the component via mutation.error
  });

  return {
    login: mutation.mutate,
    isLoading: mutation.isPending,
    isSuccess: mutation.isSuccess,
    error: mutation.error as ApiError | null,
    isError: mutation.isError,
    reset: mutation.reset,
  };
}
