import type { Config } from 'tailwindcss';
import plugin from 'tailwindcss/plugin';

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
      borderRadius: {
        none: '0px',
        sm:   'var(--radius-sm)',
        md:   'var(--radius)',
        lg:   'var(--radius-lg)',
        xl:   'var(--radius-xl)',
        '2xl':'var(--radius-2xl)',
        full: '9999px',
      },
      spacing: {
        'px':  '1px',
        '0':   '0px',
        '0.5': '0.125rem',
        '1':   '0.25rem',
        '1.5': '0.375rem',
        '2':   '0.5rem',
        '2.5': '0.625rem',
        '3':   '0.75rem',
        '3.5': '0.875rem',
        '4':   '1rem',
        '5':   '1.25rem',
        '6':   '1.5rem',
        '7':   '1.75rem',
        '8':   '2rem',
        '9':   '2.25rem',
        '10':  '2.5rem',
        '11':  '2.75rem',
        '12':  '3rem',
        '14':  '3.5rem',
        '16':  '4rem',
        '20':  '5rem',
        '24':  '6rem',
        '28':  '7rem',
        '32':  '8rem',
        '36':  '9rem',
        '40':  '10rem',
        '44':  '11rem',
        '48':  '12rem',
        '56':  '14rem',
        '60':  '15rem',
        '64':  '16rem',
        '72':  '18rem',
        '80':  '20rem',
        '96':  '24rem',
      },
      boxShadow: {
        xs:       'var(--shadow-xs)',
        sm:       'var(--shadow-sm)',
        md:       'var(--shadow-md)',
        lg:       'var(--shadow-lg)',
        xl:       'var(--shadow-xl)',
        card:     'var(--shadow-card)',
        floating: 'var(--shadow-float)',
        none:     'none',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['Geist Mono', 'ui-monospace', 'SFMono-Regular', 'monospace'],
      },
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
  plugins: [
    plugin(function({ addUtilities }) {
      addUtilities({
        /* Semantic Typography Tokens */
        '.text-display': {
          fontSize: '2.5rem',
          lineHeight: '1.1',
          letterSpacing: '-0.02em',
          fontWeight: '700',
        },
        '.text-heading-xl': {
          fontSize: '1.75rem',
          lineHeight: '1.2',
          letterSpacing: '-0.015em',
          fontWeight: '600',
        },
        '.text-heading-lg': {
          fontSize: '1.375rem',
          lineHeight: '1.3',
          letterSpacing: '-0.01em',
          fontWeight: '600',
        },
        '.text-heading-md': {
          fontSize: '1.125rem',
          lineHeight: '1.4',
          letterSpacing: '-0.005em',
          fontWeight: '600',
        },
        '.text-heading-sm': {
          fontSize: '1rem',
          lineHeight: '1.5',
          fontWeight: '600',
        },
        '.text-body-lg': {
          fontSize: '1rem',
          lineHeight: '1.6',
          fontWeight: '400',
        },
        '.text-body': {
          fontSize: '0.875rem',
          lineHeight: '1.55',
          fontWeight: '400',
        },
        '.text-caption': {
          fontSize: '0.8125rem',
          lineHeight: '1.5',
          fontWeight: '400',
        },
        '.text-label': {
          fontSize: '0.75rem',
          lineHeight: '1.4',
          fontWeight: '500',
          letterSpacing: '0.03em',
        },
        '.text-overline': {
          fontSize: '0.6875rem',
          lineHeight: '1.2',
          fontWeight: '600',
          letterSpacing: '0.08em',
        },
        '.text-mono': {
          fontSize: '0.8125rem',
          lineHeight: '1.5',
          fontWeight: '400',
        },
        '.text-number-xl': {
          fontSize: '2rem',
          lineHeight: '1',
          letterSpacing: '-0.02em',
          fontWeight: '700',
        },
        '.text-number-lg': {
          fontSize: '1.5rem',
          lineHeight: '1',
          letterSpacing: '-0.01em',
          fontWeight: '600',
        },
        '.text-number-md': {
          fontSize: '1.25rem',
          lineHeight: '1',
          fontWeight: '600',
        },

        /* Semantic Design Utilities */
        '.card-base': {
          border: '1px solid hsl(var(--border))',
          backgroundColor: 'hsl(var(--card))',
          borderRadius: 'var(--radius-lg)',
          boxShadow: 'var(--shadow-card)',
        },
        '.card-interactive': {
          border: '1px solid hsl(var(--border))',
          backgroundColor: 'hsl(var(--card))',
          borderRadius: 'var(--radius-lg)',
          boxShadow: 'var(--shadow-card)',
          transitionProperty: 'all',
          transitionDuration: 'var(--duration-normal, 160ms)',
          transitionTimingFunction: 'var(--ease-default)',
        },
        '.card-interactive:hover': {
          boxShadow: 'var(--shadow-md)',
          borderColor: 'hsl(var(--border) / 0.8)',
          transform: 'translateY(-1px)',
        },
        '.shadow-card': {
          boxShadow: 'var(--shadow-card)',
        },
        '.shadow-floating': {
          boxShadow: 'var(--shadow-float)',
        },
        '.scrollbar-hide': {
          '-ms-overflow-style': 'none',
          'scrollbar-width': 'none',
        },
        '.scrollbar-hide::-webkit-scrollbar': {
          display: 'none',
        },
        '.scrollbar-thin': {
          'scrollbar-width': 'thin',
          'scrollbar-color': 'hsl(var(--border)) transparent',
        },
      });
    }),
  ],
} satisfies Config;
