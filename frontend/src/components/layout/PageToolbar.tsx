import * as React from 'react';
import { cn } from '@/utils';

export interface PageToolbarProps extends React.HTMLAttributes<HTMLDivElement> {
  title: string;
  description?: string;
  actions?: React.ReactNode;
}

export const PageToolbar = React.forwardRef<HTMLDivElement, PageToolbarProps>(
  ({ className, title, description, actions, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn('flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between', className)}
        {...props}
      >
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground">{title}</h1>
          {description && <p className="mt-1 text-sm text-muted-foreground">{description}</p>}
        </div>
        {actions && <div className="flex items-center gap-3">{actions}</div>}
      </div>
    );
  }
);
PageToolbar.displayName = 'PageToolbar';
