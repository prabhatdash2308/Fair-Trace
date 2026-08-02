import type { Variants } from 'framer-motion';

// Standardized timings and easings per Phase 9.6 UX spec
export const TIMINGS = {
  HOVER: 0.08,           // 80ms
  CARD: 0.12,            // 120ms
  SIDEBAR: 0.16,         // 160ms
  PAGE: 0.18,            // 180ms
  COMMAND_PALETTE: 0.18, // 180ms
  MODAL: 0.22,           // 220ms
} as const;

export const EASINGS = {
  easeOut: [0.25, 0.1, 0.25, 1],
  easeInOut: [0.4, 0, 0.2, 1],
  spring: { type: 'spring', stiffness: 300, damping: 30 },
  springGentle: { type: 'spring', stiffness: 200, damping: 20 },
} as const;

export const fadeVariants: Variants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { duration: TIMINGS.PAGE, ease: EASINGS.easeInOut } },
  exit: { opacity: 0, transition: { duration: TIMINGS.PAGE, ease: EASINGS.easeInOut } },
};

export const slideUpVariants: Variants = {
  hidden: { opacity: 0, y: 12 },
  visible: { opacity: 1, y: 0, transition: { duration: TIMINGS.PAGE, ease: EASINGS.easeOut } },
  exit: { opacity: 0, y: -12, transition: { duration: TIMINGS.PAGE, ease: EASINGS.easeOut } },
};

export const slideRightVariants: Variants = {
  hidden: { opacity: 0, x: -12 },
  visible: { opacity: 1, x: 0, transition: { duration: TIMINGS.PAGE, ease: EASINGS.easeOut } },
  exit: { opacity: 0, x: 12, transition: { duration: TIMINGS.PAGE, ease: EASINGS.easeOut } },
};

export const scaleVariants: Variants = {
  hidden: { opacity: 0, scale: 0.96 },
  visible: { opacity: 1, scale: 1, transition: EASINGS.spring },
  exit: { opacity: 0, scale: 0.96, transition: { duration: TIMINGS.PAGE, ease: EASINGS.easeOut } },
};

export const modalVariants: Variants = {
  hidden: { opacity: 0, scale: 0.97, y: 10 },
  visible: { opacity: 1, scale: 1, y: 0, transition: EASINGS.spring },
  exit: { opacity: 0, scale: 0.97, y: 10, transition: { duration: TIMINGS.PAGE, ease: EASINGS.easeOut } },
};

export const sidebarVariants: Variants = {
  hidden: { x: '-100%', opacity: 0 },
  visible: { x: 0, opacity: 1, transition: EASINGS.springGentle },
  exit: { x: '-100%', opacity: 0, transition: { duration: TIMINGS.SIDEBAR, ease: EASINGS.easeInOut } },
};

export const commandPaletteVariants: Variants = {
  hidden: { opacity: 0, scale: 0.98 },
  visible: { opacity: 1, scale: 1, transition: EASINGS.spring },
  exit: { opacity: 0, scale: 0.98, transition: { duration: TIMINGS.COMMAND_PALETTE, ease: EASINGS.easeOut } },
};

export const staggerContainer: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.05,
      delayChildren: 0.02,
    },
  },
};

export const pageTransition: Variants = {
  hidden: { opacity: 0, y: 6 },
  visible: { opacity: 1, y: 0, transition: { duration: TIMINGS.PAGE, ease: EASINGS.easeInOut } },
  exit: { opacity: 0, y: -6, transition: { duration: TIMINGS.PAGE, ease: EASINGS.easeInOut } },
};

export const cardTransition: Variants = {
  hidden: { opacity: 0, y: 4 },
  visible: { opacity: 1, y: 0, transition: { duration: TIMINGS.CARD, ease: EASINGS.easeOut } }
};

export const hoverScale = {
  scale: 1.01,
  transition: { duration: TIMINGS.HOVER, ease: EASINGS.easeOut },
};

export const tapScale = {
  scale: 0.98,
  transition: { duration: TIMINGS.HOVER, ease: EASINGS.easeOut },
};
