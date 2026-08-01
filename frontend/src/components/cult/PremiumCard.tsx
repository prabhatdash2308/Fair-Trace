import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';
import type { LucideIcon } from 'lucide-react';
import type { ReactNode } from 'react';

interface PremiumCardProps {
  children?: ReactNode;
  title?: string;
  subtitle?: string;
  icon?: LucideIcon;
  badge?: string;
  className?: string;
  /** Gradient accent colour. Default: primary blue. */
  accentColor?: string;
}

/**
 * PremiumCard — Cult UI featured card with coloured accent stripe and icon.
 * Use ONLY for dashboard highlight widgets and hero sections.
 */
export function PremiumCard({
  children,
  title,
  subtitle,
  icon: Icon,
  badge,
  className,
  accentColor = 'from-primary to-blue-400',
}: PremiumCardProps) {
  return (
    <motion.div
      whileHover={{ y: -3 }}
      transition={{ duration: 0.2 }}
      className={cn(
        'relative rounded-xl border border-border bg-card overflow-hidden shadow-sm',
        className
      )}
    >
      {/* Gradient accent stripe at top */}
      <div className={cn('h-1 w-full bg-gradient-to-r', accentColor)} />

      <div className="p-6">
        {/* Header */}
        {(title ?? Icon ?? badge) && (
          <div className="flex items-start justify-between mb-4">
            <div className="flex items-center gap-3">
              {Icon && (
                <div className={cn('p-2 rounded-lg bg-gradient-to-br', accentColor, 'text-white')}>
                  <Icon className="h-4 w-4" />
                </div>
              )}
              <div>
                {title && <p className="font-semibold text-sm text-foreground">{title}</p>}
                {subtitle && <p className="text-xs text-muted-foreground mt-0.5">{subtitle}</p>}
              </div>
            </div>
            {badge && (
              <span className="text-xs font-medium px-2 py-0.5 rounded-full bg-primary/10 text-primary">
                {badge}
              </span>
            )}
          </div>
        )}

        {children}
      </div>
    </motion.div>
  );
}
