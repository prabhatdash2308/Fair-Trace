/**
 * ReviewGuard AI — Design Token System
 * Single source of truth for every spatial, typographic, motion, and color value.
 * Every component MUST consume from this file. No hardcoded values.
 *
 * Philosophy: Dense but breathable. Calm confidence. Enterprise-grade.
 */

// ─── Spacing — strict 8px grid ────────────────────────────────────────────
export const spacing = {
  px:    '1px',
  '0':   '0px',
  '0.5': '0.125rem',  // 2px
  '1':   '0.25rem',   // 4px
  '1.5': '0.375rem',  // 6px
  '2':   '0.5rem',    // 8px  ← base unit
  '2.5': '0.625rem',  // 10px
  '3':   '0.75rem',   // 12px
  '3.5': '0.875rem',  // 14px
  '4':   '1rem',      // 16px
  '5':   '1.25rem',   // 20px
  '6':   '1.5rem',    // 24px ← card padding
  '7':   '1.75rem',   // 28px
  '8':   '2rem',      // 32px ← page padding
  '10':  '2.5rem',    // 40px ← button height (default)
  '12':  '3rem',      // 48px
  '14':  '3.5rem',    // 56px ← header height
  '16':  '4rem',      // 64px
  '20':  '5rem',      // 80px
  '24':  '6rem',      // 96px
  '32':  '8rem',      // 128px
  '40':  '10rem',     // 160px
  '48':  '12rem',     // 192px
  '56':  '14rem',     // 224px
  '64':  '16rem',     // 256px ← sidebar open
} as const;

// ─── Border Radius ─────────────────────────────────────────────────────────
export const radius = {
  none: '0px',
  sm:   '6px',    // inputs, small elements
  md:   '8px',    // buttons, badges, chips
  lg:   '10px',   // cards, panels
  xl:   '12px',   // larger cards, dialogs
  '2xl':'16px',   // hero cards, modals
  full: '9999px', // avatars, pills
} as const;

// ─── Typography — semantic scale ───────────────────────────────────────────
export const typography = {
  fontFamily: {
    sans: "'Inter', 'system-ui', '-apple-system', 'sans-serif'",
    mono: "'Geist Mono', 'ui-monospace', 'SFMono-Regular', 'monospace'",
  },
  /**
   * Semantic font sizes.
   * Use THESE class names, never raw Tailwind text-xl, text-2xl, font-bold etc.
   */
  tailwindClasses: {
    display:      'text-display-xl font-bold tracking-tight',
    'heading-xl': 'text-heading-xl font-semibold tracking-tight',
    'heading-lg': 'text-heading-lg font-semibold tracking-tight',
    'heading-md': 'text-heading-md font-semibold',
    'heading-sm': 'text-heading-sm font-semibold',
    'body-lg':    'text-body-lg font-normal',
    'body':       'text-body font-normal',
    'caption':    'text-caption font-normal',
    'label':      'text-label font-medium',
    overline:     'text-[11px] font-semibold uppercase tracking-widest',
    mono:         'text-caption font-mono',
    'number-xl':  'text-heading-lg font-bold tabular-nums tracking-tight',
    'number-lg':  'text-heading-sm font-bold tabular-nums tracking-tight',
  },
} as const;

// ─── Motion — all under 250ms ──────────────────────────────────────────────
export const motion = {
  duration: {
    instant: 80,    // hover state changes (ms)
    fast:    120,   // button press, badge
    normal:  160,   // card hover, sidebar items
    page:    200,   // page transitions
    modal:   240,   // dialog, sheet
    slow:    300,   // sidebar collapse
  },
  easing: {
    default: [0.4, 0, 0.2, 1] as [number, number, number, number],
    out:     [0, 0, 0.2, 1]   as [number, number, number, number],
    in:      [0.4, 0, 1, 1]   as [number, number, number, number],
    spring:  [0.16, 1, 0.3, 1] as [number, number, number, number],
  },
} as const;

// ─── Elevation — shadows ───────────────────────────────────────────────────
export const elevation = {
  none:     'none',
  xs:       '0 1px 2px 0 rgb(0 0 0 / 0.04)',
  sm:       '0 1px 3px 0 rgb(0 0 0 / 0.06), 0 1px 2px -1px rgb(0 0 0 / 0.04)',
  md:       '0 4px 6px -1px rgb(0 0 0 / 0.07), 0 2px 4px -2px rgb(0 0 0 / 0.04)',
  lg:       '0 10px 15px -3px rgb(0 0 0 / 0.07), 0 4px 6px -4px rgb(0 0 0 / 0.04)',
  xl:       '0 20px 25px -5px rgb(0 0 0 / 0.08), 0 8px 10px -6px rgb(0 0 0 / 0.04)',
  '2xl':    '0 25px 50px -12px rgb(0 0 0 / 0.18)',
  floating: '0 0 0 1px hsl(var(--border)), 0 8px 20px -4px rgb(0 0 0 / 0.12)',
  card:     '0 0 0 1px hsl(var(--border) / 0.6), 0 1px 3px 0 rgb(0 0 0 / 0.04)',
} as const;

// ─── Z-index scale ─────────────────────────────────────────────────────────
export const zIndex = {
  base:     0,
  raised:   10,
  dropdown: 100,
  sticky:   200,
  overlay:  300,
  modal:    400,
  toast:    500,
  tooltip:  600,
} as const;

// ─── Icon sizes — Lucide icons must use these ──────────────────────────────
export const iconSize = {
  xs:   'h-3 w-3',       // 12px — badges, inline
  sm:   'h-3.5 w-3.5',   // 14px — breadcrumbs
  md:   'h-4 w-4',       // 16px — DEFAULT for nav, buttons, inputs
  lg:   'h-5 w-5',       // 20px — feature icons in cards
  xl:   'h-6 w-6',       // 24px — empty state, hero icons
  '2xl':'h-8 w-8',       // 32px — large illustrative icons
} as const;

// ─── Status color maps (semantic) ─────────────────────────────────────────
export const statusColors = {
  active:    { bg: 'bg-primary/10',  text: 'text-primary',         border: 'border-primary/20',  dot: 'bg-primary' },
  success:   { bg: 'bg-success/10',  text: 'text-success',         border: 'border-success/20',  dot: 'bg-success' },
  warning:   { bg: 'bg-warning/10',  text: 'text-warning',         border: 'border-warning/20',  dot: 'bg-warning' },
  danger:    { bg: 'bg-danger/10',   text: 'text-danger',          border: 'border-danger/20',   dot: 'bg-danger' },
  neutral:   { bg: 'bg-muted',       text: 'text-muted-foreground',border: 'border-border',       dot: 'bg-muted-foreground' },
} as const;

// ─── Layout constants ──────────────────────────────────────────────────────
export const layout = {
  headerHeight:     '56px',   // h-14
  sidebarOpen:      '240px',  // sidebar open width
  sidebarCollapsed: '56px',   // sidebar collapsed width
  pageMaxWidth:     '1280px', // max-w-screen-xl
  contentPaddingX:  '32px',   // px-8
  contentPaddingY:  '32px',   // py-8
  cardPadding:      '24px',   // p-6
  sectionGap:       '32px',   // gap-8
} as const;

// ─── Button size system ────────────────────────────────────────────────────
export const buttonSize = {
  xs:      'h-7 px-2.5 text-[11px]',  // 28px
  sm:      'h-8 px-3 text-xs',         // 32px — compact table actions
  default: 'h-10 px-4 text-sm',        // 40px — DEFAULT
  lg:      'h-11 px-5 text-sm',        // 44px — prominent CTAs
  xl:      'h-12 px-6 text-base',      // 48px — hero CTAs
  icon:    'h-10 w-10',                // icon-only default
  'icon-sm': 'h-8 w-8',               // icon-only compact
} as const;
