import * as React from 'react';
import { cn } from '@/utils';

export const ActionBar = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, children, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn('flex flex-wrap items-center gap-3 rounded-md bg-muted/30 p-2 border', className)}
        {...props}
      >
        {children}
      </div>
    );
  }
);
ActionBar.displayName = 'ActionBar';
