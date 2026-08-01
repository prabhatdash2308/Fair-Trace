import { motion } from 'framer-motion';
import { THEME_CONSTANTS } from '@/constants/theme';
import type { ReactNode } from 'react';

interface SlideInProps {
  children: ReactNode;
  direction?: 'left' | 'right' | 'up' | 'down';
  delay?: number;
  duration?: number;
  className?: string;
}

const OFFSETS: Record<string, { x?: number; y?: number }> = {
  left: { x: -24 },
  right: { x: 24 },
  up: { y: -24 },
  down: { y: 24 },
};

/**
 * SlideIn — directional slide entrance. Use for modals, sheets, drawers.
 */
export function SlideIn({
  children,
  direction = 'up',
  delay = 0,
  duration = THEME_CONSTANTS.ANIMATION.DURATION_DEFAULT,
  className,
}: SlideInProps) {
  const offset = OFFSETS[direction];

  return (
    <motion.div
      initial={{ opacity: 0, ...offset }}
      animate={{ opacity: 1, x: 0, y: 0 }}
      exit={{ opacity: 0, ...offset }}
      transition={{ duration, delay, ease: THEME_CONSTANTS.ANIMATION.EASE_DEFAULT }}
      className={className}
    >
      {children}
    </motion.div>
  );
}
