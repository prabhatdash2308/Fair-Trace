import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/utils';
import { StatusIcons } from '@/components/icons';

const statusBadgeVariants = cva(
  'inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
  {
    variants: {
      variant: {
        default: 'bg-primary/10 text-primary',
        success: 'bg-success/10 text-success',
        warning: 'bg-warning/20 text-warning-foreground',
        danger: 'bg-destructive/10 text-destructive',
        outline: 'text-foreground border border-input',
        secondary: 'bg-secondary text-secondary-foreground',
        muted: 'bg-muted text-muted-foreground',
      },
      size: {
        sm: 'px-2 py-0.5 text-[10px]',
        md: 'px-2.5 py-0.5 text-xs',
        lg: 'px-3 py-1 text-sm',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'md',
    },
  }
);

export interface StatusBadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof statusBadgeVariants> {
  icon?: keyof typeof StatusIcons | React.ElementType;
  showIcon?: boolean;
}

export const StatusBadge = React.forwardRef<HTMLDivElement, StatusBadgeProps>(
  ({ className, variant, size, icon, showIcon = true, children, ...props }, ref) => {
    // Resolve icon if passed as a string key
    let IconComponent: React.ElementType | undefined;
    if (showIcon) {
      if (typeof icon === 'string' && icon in StatusIcons) {
        IconComponent = StatusIcons[icon as keyof typeof StatusIcons];
      } else if (typeof icon !== 'string' && icon) {
        IconComponent = icon;
      }
    }

    return (
      <div
        ref={ref}
        className={cn(statusBadgeVariants({ variant, size }), className)}
        {...props}
      >
        {IconComponent && <IconComponent className={cn('h-3.5 w-3.5', size === 'sm' && 'h-3 w-3', size === 'lg' && 'h-4 w-4')} />}
        {children}
      </div>
    );
  }
);
StatusBadge.displayName = 'StatusBadge';
