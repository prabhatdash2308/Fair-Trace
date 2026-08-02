import type { Variants } from 'framer-motion';

/**
 * Standardized motion variants — ReviewGuard AI Design System.
 * Rules:
 *   - All durations: 80–240ms. Never exceed 250ms.
 *   - Movement: translateY only. Max 8px entrance, max 2px hover.
 *   - Hover: max -1px to -2px elevation, NO x-movement.
 *   - All animations must feel invisible — never flashy.
 */

// ─── Duration constants (ms ÷ 1000 for framer) ──────────────────────────
export const TIMINGS = {
  HOVER:          0.08,   // 80ms  — hover state
  FAST:           0.12,   // 120ms — button press, badge
  CARD:           0.16,   // 160ms — card hover, nav items
  PAGE:           0.20,   // 200ms — page transitions
  MODAL:          0.24,   // 240ms — dialog, sheet
  SIDEBAR:        0.28,   // 280ms — sidebar collapse
} as const;

// ─── Easing constants ─────────────────────────────────────────────────────
export const EASINGS = {
  default:  [0.4, 0, 0.2, 1]     as [number, number, number, number],
  out:      [0, 0, 0.2, 1]       as [number, number, number, number],
  easeOut:  [0, 0, 0.2, 1]       as [number, number, number, number],  // alias for backward compat
  spring:   [0.16, 1, 0.3, 1]    as [number, number, number, number],  // springy
  snappy:   [0.25, 0.1, 0.25, 1] as [number, number, number, number],
  easeInOut:[0.4, 0, 0.2, 1]     as [number, number, number, number],  // alias for backward compat
} as const;

// ─── Page / View transitions ──────────────────────────────────────────────
export const pageTransition: Variants = {
  hidden:  { opacity: 0, y: 6 },
  visible: { opacity: 1, y: 0, transition: { duration: TIMINGS.PAGE, ease: EASINGS.out } },
  exit:    { opacity: 0, y: -4, transition: { duration: TIMINGS.FAST, ease: EASINGS.default } },
};

export const fadeVariants: Variants = {
  hidden:  { opacity: 0 },
  visible: { opacity: 1, transition: { duration: TIMINGS.PAGE, ease: EASINGS.out } },
  exit:    { opacity: 0, transition: { duration: TIMINGS.FAST, ease: EASINGS.default } },
};

export const slideUpVariants: Variants = {
  hidden:  { opacity: 0, y: 8 },
  visible: { opacity: 1, y: 0, transition: { duration: TIMINGS.PAGE, ease: EASINGS.spring } },
  exit:    { opacity: 0, y: -4, transition: { duration: TIMINGS.FAST, ease: EASINGS.default } },
};

export const slideRightVariants: Variants = {
  hidden:  { opacity: 0, x: -8 },
  visible: { opacity: 1, x: 0, transition: { duration: TIMINGS.PAGE, ease: EASINGS.spring } },
  exit:    { opacity: 0, x: 8, transition: { duration: TIMINGS.FAST, ease: EASINGS.default } },
};

// ─── Card transitions ─────────────────────────────────────────────────────
export const cardTransition: Variants = {
  hidden:  { opacity: 0, y: 4 },
  visible: { opacity: 1, y: 0, transition: { duration: TIMINGS.CARD, ease: EASINGS.spring } },
};

// ─── Modal / Dialog ───────────────────────────────────────────────────────
export const modalVariants: Variants = {
  hidden:  { opacity: 0, scale: 0.97, y: 8 },
  visible: { opacity: 1, scale: 1,    y: 0, transition: { duration: TIMINGS.MODAL, ease: EASINGS.spring } },
  exit:    { opacity: 0, scale: 0.98, y: 6, transition: { duration: TIMINGS.FAST, ease: EASINGS.default } },
};

// ─── Scale (modals, popovers) ─────────────────────────────────────────────
export const scaleVariants: Variants = {
  hidden:  { opacity: 0, scale: 0.96 },
  visible: { opacity: 1, scale: 1, transition: { duration: TIMINGS.MODAL, ease: EASINGS.spring } },
  exit:    { opacity: 0, scale: 0.98, transition: { duration: TIMINGS.FAST, ease: EASINGS.default } },
};

// ─── Command palette ──────────────────────────────────────────────────────
export const commandPaletteVariants: Variants = {
  hidden:  { opacity: 0, scale: 0.97, y: -12 },
  visible: { opacity: 1, scale: 1, y: 0, transition: { duration: TIMINGS.MODAL, ease: EASINGS.spring } },
  exit:    { opacity: 0, scale: 0.98, y: -8, transition: { duration: TIMINGS.FAST, ease: EASINGS.default } },
};

// ─── Sidebar ─────────────────────────────────────────────────────────────
export const sidebarVariants: Variants = {
  hidden:  { x: '-100%', opacity: 0 },
  visible: { x: 0, opacity: 1, transition: { duration: TIMINGS.SIDEBAR, ease: EASINGS.default } },
  exit:    { x: '-100%', opacity: 0, transition: { duration: TIMINGS.SIDEBAR, ease: EASINGS.default } },
};

// ─── Stagger container ────────────────────────────────────────────────────
export const staggerContainer: Variants = {
  hidden:  { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.04,
      delayChildren:   0.02,
    },
  },
};

// ─── Hover / Tap (Framer motion whileHover / whileTap props) ─────────────
/** Card elevation hover — max 2px per spec */
export const hoverScale = {
  y: -1,
  transition: { duration: TIMINGS.CARD, ease: EASINGS.out },
};

/** Button tap / click depress */
export const tapScale = {
  scale: 0.97,
  transition: { duration: TIMINGS.HOVER },
};

/** List item hover — very subtle */
export const listItemHover = {
  x: 1,
  transition: { duration: TIMINGS.HOVER, ease: EASINGS.out },
};
