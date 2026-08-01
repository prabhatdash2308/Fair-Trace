import { cn } from '@/lib/utils';
import type { ReactNode } from 'react';

interface GradientBorderProps {
  children: ReactNode;
  className?: string;
  /** Gradient colour stops. Default: primary blue. */
  gradient?: string;
  borderWidth?: 1 | 2;
  borderRadius?: 'md' | 'lg' | 'xl';
}

const RADIUS = { md: 'rounded-md', lg: 'rounded-lg', xl: 'rounded-xl' };

/**
 * GradientBorder — wraps any element in an animated gradient border.
 * Use ONLY for: CTAs, empty states, landing page highlights.
 */
export function GradientBorder({
  children,
  className,
  gradient = 'from-primary via-blue-400 to-indigo-600',
  borderWidth = 1,
  borderRadius = 'lg',
}: GradientBorderProps) {
  return (
    <div
      className={cn(
        'relative inline-flex',
        RADIUS[borderRadius],
        className
      )}
      style={{ padding: borderWidth }}
    >
      {/* Gradient background layer */}
      <div
        aria-hidden="true"
        className={cn(
          'absolute inset-0 bg-gradient-to-r',
          gradient,
          RADIUS[borderRadius]
        )}
      />
      {/* Content layer */}
      <div className={cn('relative bg-card w-full', RADIUS[borderRadius])}>
        {children}
      </div>
    </div>
  );
}
