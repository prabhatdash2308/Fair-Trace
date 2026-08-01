import { motion, AnimatePresence } from 'framer-motion';
import { useLocation } from 'react-router-dom';
import { THEME_CONSTANTS } from '@/constants/theme';
import type { ReactNode } from 'react';

interface PageTransitionProps {
  children: ReactNode;
}

/**
 * PageTransition — wraps page content with a smooth entrance animation.
 * Keyed by pathname so it re-triggers on route change.
 */
export function PageTransition({ children }: PageTransitionProps) {
  const { pathname } = useLocation();

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={pathname}
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -8 }}
        transition={{
          duration: THEME_CONSTANTS.ANIMATION.DURATION_DEFAULT,
          ease: THEME_CONSTANTS.ANIMATION.EASE_DEFAULT,
        }}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  );
}
