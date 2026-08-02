import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';
import type { ReactNode } from 'react';

interface PageHeaderProps {
  title: string;
  subtitle?: string;
  actions?: ReactNode;
  className?: string;
  /** Optional eyebrow text above the title (e.g. "Q3 2026") */
  eyebrow?: string;
}

/**
 * PageHeader — standardized top-of-page header.
 * Every page uses this exact component. No exceptions.
 *
 * Layout:
 *   [eyebrow?]
 *   [title]       [actions]
 *   [subtitle?]
 *   ────────── border ──────────
 *   (mb-8 gap below for content)
 */
export function PageHeader({ title, subtitle, actions, className, eyebrow }: PageHeaderProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: -4 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
      className={cn('mb-8', className)}
    >
      <div className="flex items-start justify-between gap-4 pb-6 border-b border-border">
        <div className="min-w-0 flex-1">
          {eyebrow && (
            <p className="text-overline text-muted-foreground uppercase tracking-widest mb-1">
              {eyebrow}
            </p>
          )}
          <h1 className="text-heading-xl font-semibold text-foreground tracking-tight truncate">
            {title}
          </h1>
          {subtitle && (
            <p className="mt-1 text-body text-muted-foreground leading-relaxed max-w-2xl">
              {subtitle}
            </p>
          )}
        </div>

        {actions && (
          <div className="flex items-center gap-2 shrink-0 mt-0.5">
            {actions}
          </div>
        )}
      </div>
    </motion.div>
  );
}
