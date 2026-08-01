import * as React from 'react';
import { cn } from '@/utils';

export interface PageSectionProps extends React.HTMLAttributes<HTMLElement> {
  title?: string;
  description?: string;
  actions?: React.ReactNode;
}

export const PageSection = React.forwardRef<HTMLElement, PageSectionProps>(
  ({ className, title, description, actions, children, ...props }, ref) => {
    return (
      <section ref={ref} className={cn('space-y-4', className)} {...props}>
        {(title || actions) && (
          <div className="flex items-center justify-between pb-2">
            <div>
              {title && <h2 className="text-lg font-semibold tracking-tight">{title}</h2>}
              {description && <p className="text-sm text-muted-foreground">{description}</p>}
            </div>
            {actions && <div className="flex items-center gap-2">{actions}</div>}
          </div>
        )}
        {children}
      </section>
    );
  }
);
PageSection.displayName = 'PageSection';
