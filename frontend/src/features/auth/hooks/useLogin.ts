import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import { authService } from '../services/auth.service';
import { roleDashboardRoute } from '@/constants/routes';
import { useAuthStore } from '@/store/auth/auth.store';
import { DEMO_MODE, DEMO_USER, DEMO_TOKEN } from '@/config/demo';
import type { LoginSchema } from '../schemas/login.schema';
import type { ApiError } from '@/types';

/**
 * useLogin — TanStack Query mutation hook for the login flow.
 *
 * In DEMO_MODE: skips the API call entirely, instantly injects the demo
 * admin user into the auth store, and navigates to the admin dashboard.
 *
 * In production: calls authService.login → backend → JWT flow.
 */
export function useLogin() {
  const navigate = useNavigate();
  const location = useLocation();
  const { login: storeLogin } = useAuthStore();
  const [isDemoLoading, setIsDemoLoading] = useState(false);

  const from =
    (location.state as { from?: { pathname: string } })?.from?.pathname ?? null;

  // ── DEMO MODE ────────────────────────────────────────────────────────────────
  if (DEMO_MODE) {
    const demoLogin = (_values: LoginSchema) => {
      setIsDemoLoading(true);
      // Brief visual delay so it feels like a real login
      setTimeout(() => {
        storeLogin(DEMO_TOKEN, DEMO_USER);
        const destination = from ?? roleDashboardRoute(DEMO_USER.role);
        navigate(destination, { replace: true });
        setIsDemoLoading(false);
      }, 600);
    };

    return {
      login: demoLogin,
      isLoading: isDemoLoading,
      isSuccess: false,
      error: null,
      isError: false,
      reset: () => {},
    };
  }

  // ── PRODUCTION MODE ──────────────────────────────────────────────────────────
  // eslint-disable-next-line react-hooks/rules-of-hooks
  const mutation = useMutation({
    mutationFn: ({ email, password, rememberMe }: LoginSchema) =>
      authService.login({ email, password }, rememberMe),

    onSuccess: (response) => {
      const roleTarget = roleDashboardRoute(response.user.role);
      const destination = from ?? roleTarget;
      navigate(destination, { replace: true });
    },
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
