import { motion } from 'framer-motion';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { cn } from '@/lib/utils';

interface MetricTrend {
  direction: 'up' | 'down' | 'neutral';
  value: number;
  label?: string;
}

interface MetricCardProps {
  title: string;
  value: string | number;
  description?: string;
  icon?: React.ElementType;
  trend?: MetricTrend;
  variant?: 'default' | 'success' | 'warning' | 'danger' | 'info';
  loading?: boolean;
  className?: string;
}

const ACCENT_BORDER = {
  default: 'border-t-primary/40',
  success: 'border-t-success/40',
  warning: 'border-t-warning/40',
  danger:  'border-t-danger/40',
  info:    'border-t-info/40',
} as const;

const ICON_STYLE = {
  default: 'bg-primary/10 text-primary',
  success: 'bg-success/10 text-success',
  warning: 'bg-warning/10 text-warning',
  danger:  'bg-danger/10 text-danger',
  info:    'bg-info/10 text-info',
} as const;

const TREND_CONFIG = {
  up:      { Icon: TrendingUp,   color: 'text-success' },
  down:    { Icon: TrendingDown, color: 'text-danger'  },
  neutral: { Icon: Minus,        color: 'text-muted-foreground' },
} as const;

/**
 * MetricCard — KPI display. Enterprise standard.
 * Uses semantic number tokens for values.
 * Subtle top border accent indicates metric type.
 * Trend indicators using semantic colors.
 * max 1px hover elevation per motion spec.
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
  // Loading skeleton
  if (loading) {
    return (
      <div className={cn(
        'rounded-lg border border-border bg-card p-6',
        'shadow-card space-y-3',
        className
      )}>
        <div className="flex items-center justify-between">
          <div className="h-3 w-20 rounded-md animate-shimmer" />
          <div className="h-8 w-8 rounded-lg animate-shimmer shrink-0" />
        </div>
        <div className="h-8 w-16 rounded-md animate-shimmer" />
        <div className="h-2.5 w-28 rounded-md animate-shimmer" />
      </div>
    );
  }

  const TrendMeta = trend ? TREND_CONFIG[trend.direction] : null;

  return (
    <motion.div
      whileHover={{ y: -1 }}
      transition={{ duration: 0.16, ease: [0.4, 0, 0.2, 1] }}
      className={cn(
        'rounded-lg border border-border border-t-2 bg-card text-card-foreground',
        'shadow-card p-6',
        'transition-shadow duration-[160ms]',
        'hover:shadow-md',
        ACCENT_BORDER[variant],
        className
      )}
    >
      <div className="flex items-start justify-between gap-3">
        {/* Content */}
        <div className="flex-1 min-w-0 space-y-1">
          <p className="text-overline text-muted-foreground uppercase tracking-widest truncate">
            {title}
          </p>
          <p className="text-number-xl tabular-nums leading-none text-foreground">
            {value}
          </p>

          {description && (
            <p className="text-caption text-muted-foreground truncate">{description}</p>
          )}

          {trend && TrendMeta && (
            <div className={cn('flex items-center gap-1 text-caption font-medium pt-0.5', TrendMeta.color)}>
              <TrendMeta.Icon className="h-3.5 w-3.5 shrink-0" />
              <span>
                {trend.value > 0 ? '+' : ''}{trend.value}%
              </span>
              {trend.label && (
                <span className="text-muted-foreground font-normal">{trend.label}</span>
              )}
            </div>
          )}
        </div>

        {/* Icon */}
        {Icon && (
          <div className={cn(
            'p-2 rounded-lg shrink-0',
            ICON_STYLE[variant]
          )}>
            <Icon className="h-4 w-4" aria-hidden="true" />
          </div>
        )}
      </div>
    </motion.div>
  );
}
