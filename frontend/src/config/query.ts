import type { DefaultOptions } from '@tanstack/react-query';

/**
 * Global React Query defaults.
 * Centralizes all caching, retry, and staleness behaviour.
 */
export const queryConfig: DefaultOptions = {
  queries: {
    staleTime: 1000 * 60 * 5,      // 5 minutes
    gcTime: 1000 * 60 * 30,         // 30 minutes
    refetchOnWindowFocus: false,
    refetchOnReconnect: true,
    retry: (failureCount, error: unknown) => {
      const status = (error as { response?: { status?: number } })?.response?.status;
      if (status === 401 || status === 403 || status === 404) return false;
      return failureCount < 2;
    },
    retryDelay: (attempt) => Math.min(1000 * 2 ** attempt, 30000),
  },
  mutations: {
    retry: false,
  },
};
