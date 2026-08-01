import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';
import type { PageHeaderProps } from '@/types/ui.types';

/**
 * PageHeader — standardised page title + subtitle + optional action slot.
 * Place at the top of every page, below Breadcrumbs.
 */
export function PageHeader({ title, subtitle, actions, className }: PageHeaderProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: -4 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.2 }}
      className={cn('flex items-start justify-between gap-4 mb-6', className)}
    >
      <div className="min-w-0">
        <h1 className="text-2xl font-bold text-foreground tracking-tight truncate">{title}</h1>
        {subtitle && (
          <p className="mt-1 text-sm text-muted-foreground">{subtitle}</p>
        )}
      </div>

      {actions && (
        <div className="flex items-center gap-2 shrink-0">{actions}</div>
      )}
    </motion.div>
  );
}
