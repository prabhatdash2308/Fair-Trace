import * as React from 'react';
import { ResponsiveGrid } from './ResponsiveGrid';
import { cn } from '@/utils';

export const StatGrid = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, children, ...props }, ref) => {
    return (
      <ResponsiveGrid ref={ref} columns={4} gap="md" className={cn('mb-6', className)} {...props}>
        {children}
      </ResponsiveGrid>
    );
  }
);
StatGrid.displayName = 'StatGrid';
