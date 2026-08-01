import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';
import type { ReactNode } from 'react';

interface GlassCardProps {
  children: ReactNode;
  className?: string;
  /** Whether to apply the subtle hover lift animation. Default: true. */
  hoverable?: boolean;
  /** Internal padding preset. Default: 'md'. */
  padding?: 'sm' | 'md' | 'lg';
}

const PADDING = { sm: 'p-4', md: 'p-6', lg: 'p-8' };

/**
 * GlassCard — Cult UI premium card.
 * Use ONLY for: hero sections, dashboard highlight widgets, landing page.
 * Do NOT scatter throughout the app.
 *
 * Design: Subtle background blur, refined border, hover lift.
 */
export function GlassCard({
  children,
  className,
  hoverable = true,
  padding = 'md',
}: GlassCardProps) {
  return (
    <motion.div
      whileHover={hoverable ? { y: -2, scale: 1.005 } : undefined}
      transition={{ duration: 0.2 }}
      className={cn(
        // Base
        'rounded-xl border bg-card/80 backdrop-blur-sm',
        // Subtle gradient overlay
        'relative overflow-hidden',
        // Border
        'border-white/10 dark:border-white/[0.06]',
        // Shadow
        'shadow-sm hover:shadow-md transition-shadow duration-300',
        // Padding
        PADDING[padding],
        className
      )}
    >
      {/* Subtle top-edge glow */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-primary/20 to-transparent"
      />
      {children}
    </motion.div>
  );
}
