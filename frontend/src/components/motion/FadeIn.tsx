import { motion } from 'framer-motion';
import { THEME_CONSTANTS } from '@/constants/theme';
import type { ReactNode } from 'react';

interface FadeInProps {
  children: ReactNode;
  delay?: number;
  duration?: number;
  className?: string;
}

/**
 * FadeIn — simple opacity + vertical translate entrance.
 * Use for page sections, cards, and list items.
 */
export function FadeIn({
  children,
  delay = 0,
  duration = THEME_CONSTANTS.ANIMATION.DURATION_DEFAULT,
  className,
}: FadeInProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 8 }}
      transition={{ duration, delay, ease: THEME_CONSTANTS.ANIMATION.EASE_DEFAULT }}
      className={className}
    >
      {children}
    </motion.div>
  );
}
