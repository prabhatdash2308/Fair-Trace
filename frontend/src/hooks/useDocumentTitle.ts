import { useEffect } from 'react';

const APP_NAME = 'ReviewGuard AI';

/**
 * useDocumentTitle — sets the browser tab title.
 * Appends the app name suffix for consistency.
 *
 * @param title - The page-specific title. Pass empty string to show only the app name.
 */
export function useDocumentTitle(title: string): void {
  useEffect(() => {
    const previous = document.title;
    document.title = title ? `${title} — ${APP_NAME}` : APP_NAME;
    return () => {
      document.title = previous;
    };
  }, [title]);
}
