import { useEffect, useCallback } from 'react';
import { useThemeStore } from '@/store/theme/theme.store';
import type { Theme } from '@/config/theme';

/**
 * useTheme — reads and updates the active theme.
 * Initialises the HTML class on first mount from persisted preference.
 */
export function useTheme() {
  const { theme, resolvedTheme, setTheme, toggleTheme } = useThemeStore();

  // Hydrate DOM on first render
  useEffect(() => {
    document.documentElement.classList.toggle('dark', resolvedTheme === 'dark');
  }, [resolvedTheme]);

  const changeTheme = useCallback(
    (next: Theme) => {
      setTheme(next);
    },
    [setTheme]
  );

  return { theme, resolvedTheme, setTheme: changeTheme, toggleTheme };
}
