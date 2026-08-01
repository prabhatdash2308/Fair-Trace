import { useEffect, type ReactNode } from 'react';
import { useThemeStore } from '@/store/theme/theme.store';

interface ThemeProviderProps {
  children: ReactNode;
}

/**
 * ThemeProvider — hydrates the DOM dark class from persisted theme on first render.
 * Must wrap the entire app so children always see a stable theme.
 */
export function ThemeProvider({ children }: ThemeProviderProps) {
  const { resolvedTheme } = useThemeStore();

  useEffect(() => {
    document.documentElement.classList.toggle('dark', resolvedTheme === 'dark');
  }, [resolvedTheme]);

  return <>{children}</>;
}
