import { useMutation } from '@tanstack/react-query';
import { useNavigate, useLocation } from 'react-router-dom';
import { authService } from '../services/auth.service';
import { ROUTES } from '@/constants/routes';
import type { LoginSchema } from '../schemas/login.schema';
import type { ApiError } from '@/types';

/**
 * useLogin — TanStack Query mutation hook for the login flow.
 *
 * Responsibilities (in order):
 *  1. Call authService.login (handles API + store + persistence)
 *  2. Redirect to the originally requested page (or /dashboard)
 *  3. Surface API errors to the calling component
 */
export function useLogin() {
  const navigate = useNavigate();
  const location = useLocation();

  // The page the user was trying to reach before being redirected to /login
  const from =
    (location.state as { from?: { pathname: string } })?.from?.pathname ??
    ROUTES.DASHBOARD;

  const mutation = useMutation({
    mutationFn: ({ email, password, rememberMe }: LoginSchema) =>
      authService.login({ email, password }, rememberMe),

    onSuccess: () => {
      navigate(from, { replace: true });
    },

    // onError is handled by the component via mutation.error
  });

  return {
    login: mutation.mutate,
    isLoading: mutation.isPending,
    error: mutation.error as ApiError | null,
    isError: mutation.isError,
    reset: mutation.reset,
  };
}
