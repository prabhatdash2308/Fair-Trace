import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import type { LucideIcon } from 'lucide-react';

interface EmptyStateAction {
  label: string;
  onClick?: () => void;
  href?: string;
  variant?: 'default' | 'outline' | 'ghost';
}

interface EmptyStateProps {
  icon?: LucideIcon;
  title: string;
  description?: string;
  action?: EmptyStateAction;
  secondaryAction?: EmptyStateAction;
  className?: string;
  size?: 'sm' | 'md' | 'lg';
}

const sizeConfig = {
  sm: { wrapper: 'py-10', icon: 'h-5 w-5', iconBox: 'p-2.5 mb-3', title: 'text-heading-sm', desc: 'text-caption' },
  md: { wrapper: 'py-16', icon: 'h-6 w-6', iconBox: 'p-3 mb-4',   title: 'text-heading-md', desc: 'text-body' },
  lg: { wrapper: 'py-24', icon: 'h-8 w-8', iconBox: 'p-4 mb-5',   title: 'text-heading-lg', desc: 'text-body-lg' },
};

/**
 * EmptyState — premium empty state with icon, headline, description, and CTA(s).
 * Never show blank white space. Every empty state must feel informative and actionable.
 */
export function EmptyState({
  icon: Icon,
  title,
  description,
  action,
  secondaryAction,
  className,
  size = 'md',
}: EmptyStateProps) {
  const cfg = sizeConfig[size];

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
      className={cn(
        'flex flex-col items-center justify-center text-center px-6',
        cfg.wrapper,
        className
      )}
      aria-live="polite"
    >
      {Icon && (
        <div className={cn(
          'rounded-xl bg-muted/70 border border-border/60 flex items-center justify-center',
          cfg.iconBox
        )}>
          <Icon className={cn(cfg.icon, 'text-muted-foreground/70')} aria-hidden="true" />
        </div>
      )}

      <h3 className={cn(cfg.title, 'text-foreground font-semibold mb-1.5 text-balance')}>{title}</h3>

      {description && (
        <p className={cn(cfg.desc, 'text-muted-foreground max-w-sm leading-relaxed mb-6 text-balance')}>
          {description}
        </p>
      )}

      {(action || secondaryAction) && (
        <div className="flex items-center gap-3 flex-wrap justify-center">
          {action && (
            <Button
              id="empty-state-primary-cta"
              variant={action.variant ?? 'default'}
              size="sm"
              onClick={action.onClick}
            >
              {action.label}
            </Button>
          )}
          {secondaryAction && (
            <Button
              id="empty-state-secondary-cta"
              variant={secondaryAction.variant ?? 'ghost'}
              size="sm"
              onClick={secondaryAction.onClick}
            >
              {secondaryAction.label}
            </Button>
          )}
        </div>
      )}
    </motion.div>
  );
}
