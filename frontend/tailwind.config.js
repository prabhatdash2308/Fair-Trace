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
        // Enterprise brand aliases (for non-CSS-var contexts)
        'brand-blue':    '#2563EB',
        'brand-emerald': '#10B981',
        'brand-amber':   '#F59E0B',
        'brand-rose':    '#F43F5E',
        'brand-indigo':  '#6366F1',
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
      spacing: {
        '32': '8rem',
        '40': '10rem',
        '48': '12rem',
        '64': '16rem',
      },

      // ── Shadows ───────────────────────────────────────────────────────
      boxShadow: {
        floating: '0 0 0 1px rgba(0,0,0,0.05), 0 8px 20px -4px rgba(0,0,0,0.1)',
        glass: '0 4px 30px rgba(0, 0, 0, 0.1)',
      },

      // ── Typography — Geist ────────────────────────────────────────────
      fontFamily: {
        sans: ['Geist', 'Inter', 'system-ui', 'sans-serif'],
        mono: ['Geist Mono', 'ui-monospace', 'SFMono-Regular', 'monospace'],
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
