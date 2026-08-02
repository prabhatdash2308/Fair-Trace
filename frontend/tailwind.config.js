/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ['class'],
  content: [
    './index.html',
    './src/**/*.{ts,tsx}',
  ],
  theme: {
    container: {
      center: true,
      padding: '2rem',
      screens: { '2xl': '1400px' },
    },
    extend: {
      // ── Colours (CSS variable–driven) ────────────────────────────────
      colors: {
        border:      'hsl(var(--border))',
        input:       'hsl(var(--input))',
        ring:        'hsl(var(--ring))',
        background:  'hsl(var(--background))',
        foreground:  'hsl(var(--foreground))',
        primary: {
          DEFAULT:    'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))',
        },
        secondary: {
          DEFAULT:    'hsl(var(--secondary))',
          foreground: 'hsl(var(--secondary-foreground))',
        },
        destructive: {
          DEFAULT:    'hsl(var(--destructive))',
          foreground: 'hsl(var(--destructive-foreground))',
        },
        muted: {
          DEFAULT:    'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))',
        },
        accent: {
          DEFAULT:    'hsl(var(--accent))',
          foreground: 'hsl(var(--accent-foreground))',
        },
        popover: {
          DEFAULT:    'hsl(var(--popover))',
          foreground: 'hsl(var(--popover-foreground))',
        },
        card: {
          DEFAULT:    'hsl(var(--card))',
          foreground: 'hsl(var(--card-foreground))',
        },
        // Semantic tokens
        success: {
          DEFAULT:    'hsl(var(--success))',
          foreground: 'hsl(var(--success-foreground))',
        },
        warning: {
          DEFAULT:    'hsl(var(--warning))',
          foreground: 'hsl(var(--warning-foreground))',
        },
        danger: {
          DEFAULT:    'hsl(var(--danger))',
          foreground: 'hsl(var(--danger-foreground))',
        },
        surface: {
          DEFAULT:    'hsl(var(--surface))',
          secondary:  'hsl(var(--surface-secondary))',
        },
      },

      // ── Border Radius ─────────────────────────────────────────────────
      borderRadius: {
        lg:   'var(--radius)',
        md:   'calc(var(--radius) - 2px)',
        sm:   'calc(var(--radius) - 4px)',
        xl:   'calc(var(--radius) + 4px)',
        '2xl':'calc(var(--radius) + 8px)',
      },

      // ── Spacing ───────────────────────────────────────────────────────
      // Strict token scale: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96
      spacing: {
        '1': '0.25rem',  // 4px
        '2': '0.5rem',   // 8px
        '3': '0.75rem',  // 12px
        '4': '1rem',     // 16px
        '5': '1.25rem',  // 20px
        '6': '1.5rem',   // 24px
        '8': '2rem',     // 32px
        '10': '2.5rem',  // 40px
        '12': '3rem',    // 48px
        '16': '4rem',    // 64px
        '20': '5rem',    // 80px
        '24': '6rem',    // 96px
      },

      // ── Shadows ───────────────────────────────────────────────────────
      boxShadow: {
        sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        floating: '0 0 0 1px rgba(0,0,0,0.05), 0 8px 20px -4px rgba(0,0,0,0.1)',
        glass: '0 4px 30px rgba(0, 0, 0, 0.1)',
      },

      // ── Typography — Geist ────────────────────────────────────────────
      fontFamily: {
        sans: ['Geist', 'Inter', 'system-ui', 'sans-serif'],
        mono: ['Geist Mono', 'ui-monospace', 'SFMono-Regular', 'monospace'],
      },
      fontSize: {
        // Semantic Typography Tokens
        'display-xl': ['4.5rem',   { lineHeight: '1.05', letterSpacing: '-0.025em', fontWeight: '700' }],
        'display-lg': ['3.75rem',  { lineHeight: '1.05', letterSpacing: '-0.02em',  fontWeight: '700' }],
        'heading-xl': ['3rem',     { lineHeight: '1.15', letterSpacing: '-0.015em', fontWeight: '600' }],
        'heading-lg': ['2.25rem',  { lineHeight: '1.2',  letterSpacing: '-0.01em',  fontWeight: '600' }],
        'heading-md': ['1.875rem', { lineHeight: '1.3',  fontWeight: '600' }],
        'heading-sm': ['1.5rem',   { lineHeight: '1.35', fontWeight: '600' }],
        'body-lg':    ['1.125rem', { lineHeight: '1.6',  fontWeight: '400' }],
        'body':       ['1rem',     { lineHeight: '1.5',  fontWeight: '400' }],
        'caption':    ['0.875rem', { lineHeight: '1.5',  fontWeight: '400' }],
        'label':      ['0.75rem',  { lineHeight: '1',    fontWeight: '500', letterSpacing: '0.05em' }],
      },

      // ── Keyframes & Animations ────────────────────────────────────────
      keyframes: {
        'accordion-down': {
          from: { height: '0' },
          to:   { height: 'var(--radix-accordion-content-height)' },
        },
        'accordion-up': {
          from: { height: 'var(--radix-accordion-content-height)' },
          to:   { height: '0' },
        },
        'fade-in': {
          from: { opacity: '0' },
          to:   { opacity: '1' },
        },
        'slide-up': {
          from: { opacity: '0', transform: 'translateY(8px)' },
          to:   { opacity: '1', transform: 'translateY(0)' },
        },
        'slide-in-from-right': {
          from: { opacity: '0', transform: 'translateX(8px)' },
          to:   { opacity: '1', transform: 'translateX(0)' },
        },
      },
      animation: {
        'accordion-down':       'accordion-down 0.2s ease-out',
        'accordion-up':         'accordion-up 0.2s ease-out',
        'fade-in':              'fade-in 0.2s ease',
        'slide-up':             'slide-up 0.25s ease',
        'slide-in-from-right':  'slide-in-from-right 0.25s ease',
      },
    },
  },
  plugins: [],
};
