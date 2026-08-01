import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { queryConfig } from '@/config/query';
import type { ReactNode } from 'react';

const queryClient = new QueryClient({ defaultOptions: queryConfig });

interface QueryProviderProps {
  children: ReactNode;
}

/**
 * QueryProvider — wraps the app in TanStack React Query.
 * Uses the centralised queryConfig defaults.
 */
export function QueryProvider({ children }: QueryProviderProps) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}

// Export client for imperative usage (e.g., invalidation after mutations)
export { queryClient };
