/**
 * Design token colours — matches Tailwind config and CSS variables.
 * Used for dynamic colour injection (e.g. Recharts, canvas).
 */
export const colors = {
  primary: { DEFAULT: 'hsl(221 83% 53%)', foreground: 'hsl(210 40% 98%)' },
  secondary: { DEFAULT: 'hsl(215 25% 27%)', foreground: 'hsl(210 40% 98%)' },

  success: { DEFAULT: 'hsl(160 84% 39%)', foreground: 'hsl(0 0% 100%)' },
  warning: { DEFAULT: 'hsl(38 92% 50%)', foreground: 'hsl(0 0% 0%)' },
  danger:  { DEFAULT: 'hsl(347 77% 50%)', foreground: 'hsl(0 0% 100%)' },

  // Semantic aliases
  brand:   '#2563EB',
  teal:    '#14B8A6',
  amber:   '#F59E0B',
  rose:    '#F43F5E',
  emerald: '#10B981',
  indigo:  '#6366F1',

  // Chart palette (Recharts)
  chart: ['#2563EB', '#10B981', '#F59E0B', '#F43F5E', '#6366F1', '#14B8A6'],
} as const;
