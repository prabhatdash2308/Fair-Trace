import { motion } from 'framer-motion';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { cn } from '@/lib/utils';
import type { MetricCardProps } from '@/types/ui.types';

const VARIANT_STYLES = {
  default: 'border-border',
  success: 'border-emerald-500/30',
  warning: 'border-amber-500/30',
  danger: 'border-rose-500/30',
  info: 'border-blue-500/30',
};

const ICON_BG = {
  default: 'bg-primary/10 text-primary',
  success: 'bg-emerald-500/10 text-emerald-500',
  warning: 'bg-amber-500/10 text-amber-500',
  danger: 'bg-rose-500/10 text-rose-500',
  info: 'bg-blue-500/10 text-blue-500',
};

const TREND_ICON = {
  up: TrendingUp,
  down: TrendingDown,
  neutral: Minus,
};

const TREND_COLOUR = {
  up: 'text-emerald-500',
  down: 'text-rose-500',
  neutral: 'text-muted-foreground',
};

/**
 * MetricCard — KPI display card with icon, value, optional trend.
 * Standard card for all dashboard metric grids.
 */
export function MetricCard({
  title,
  value,
  description,
  icon: Icon,
  trend,
  variant = 'default',
  loading = false,
  className,
}: MetricCardProps) {
  if (loading) {
    return (
      <div className={cn('rounded-xl border border-border bg-card p-6 animate-pulse', className)}>
        <div className="h-4 w-24 bg-muted rounded mb-4" />
        <div className="h-8 w-16 bg-muted rounded mb-2" />
        <div className="h-3 w-32 bg-muted rounded" />
      </div>
    );
  }

  const TrendIcon = trend ? TREND_ICON[trend.direction] : null;

  return (
    <motion.div
      whileHover={{ y: -2 }}
      transition={{ duration: 0.2 }}
      className={cn(
        'rounded-xl border bg-card p-6 transition-shadow hover:shadow-md',
        VARIANT_STYLES[variant],
        className
      )}
    >
      <div className="flex items-start justify-between">
        <div className="space-y-1 flex-1 min-w-0">
          <p className="text-sm font-medium text-muted-foreground truncate">{title}</p>
          <p className="text-2xl font-bold text-foreground tabular-nums">{value}</p>
          {description && (
            <p className="text-xs text-muted-foreground truncate">{description}</p>
          )}
          {trend && TrendIcon && (
            <div className={cn('flex items-center gap-1 text-xs font-medium', TREND_COLOUR[trend.direction])}>
              <TrendIcon className="h-3.5 w-3.5" />
              <span>{trend.value > 0 ? '+' : ''}{trend.value}%</span>
              {trend.label && <span className="text-muted-foreground font-normal">{trend.label}</span>}
            </div>
          )}
        </div>

        {Icon && (
          <div className={cn('p-2.5 rounded-lg ml-4 shrink-0', ICON_BG[variant])}>
            <Icon className="h-5 w-5" />
          </div>
        )}
      </div>
    </motion.div>
  );
}
