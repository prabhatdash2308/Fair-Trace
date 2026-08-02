/**
 * Design system theme constants.
 * Synchronised with tailwind.config.js extended theme.
 */
export const THEME_CONSTANTS = {
  STORAGE_KEY: 'rg_theme',
  DEFAULT: 'light',

  BREAKPOINTS: {
    sm: 640,
    md: 768,
    lg: 1024,
    xl: 1280,
    '2xl': 1536,
  },

  SIDEBAR: {
    OPEN_WIDTH: 260,
    COLLAPSED_WIDTH: 72,
    TRANSITION_DURATION: 0.25,
  },

  ANIMATION: {
    DURATION_FAST: 0.15,
    DURATION_DEFAULT: 0.25,
    DURATION_SLOW: 0.4,
    EASE_DEFAULT: [0.4, 0, 0.2, 1],
  },
} as const;
