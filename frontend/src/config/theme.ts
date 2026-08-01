/**
 * Theme configuration — colours, radius, and spacing tokens.
 * Used as the single source of truth for both Tailwind config and runtime theming.
 */
export const themeConfig = {
  colors: {
    primary: {
      DEFAULT: 'hsl(221, 83%, 53%)',     // Blue-600
      foreground: 'hsl(210, 40%, 98%)',
    },
    secondary: {
      DEFAULT: 'hsl(215, 25%, 27%)',     // Slate-700
      foreground: 'hsl(210, 40%, 98%)',
    },
    success: {
      DEFAULT: 'hsl(160, 84%, 39%)',     // Emerald-600
      foreground: 'hsl(0, 0%, 100%)',
    },
    warning: {
      DEFAULT: 'hsl(38, 92%, 50%)',      // Amber-500
      foreground: 'hsl(0, 0%, 0%)',
    },
    danger: {
      DEFAULT: 'hsl(347, 77%, 50%)',     // Rose-600
      foreground: 'hsl(0, 0%, 100%)',
    },
  },
  radius: {
    sm: '0.25rem',
    md: '0.5rem',
    lg: '0.75rem',
    xl: '1rem',
    '2xl': '1.5rem',
  },
  defaultTheme: 'dark' as const,
} as const;

export type Theme = 'light' | 'dark' | 'system';
