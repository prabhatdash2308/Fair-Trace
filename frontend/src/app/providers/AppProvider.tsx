import type { ReactNode } from 'react';
import { QueryProvider } from './QueryProvider';
import { ThemeProvider } from './ThemeProvider';

interface AppProviderProps {
  children: ReactNode;
}

/**
 * AppProvider — composes all providers in the correct dependency order.
 * ThemeProvider must be outermost so all children see the correct theme.
 * QueryProvider wraps content so data hooks are always available.
 *
 * Adding a new provider? Add it here — never nest providers in page components.
 */
export function AppProvider({ children }: AppProviderProps) {
  return (
    <ThemeProvider>
      <QueryProvider>
        {children}
      </QueryProvider>
    </ThemeProvider>
  );
}
