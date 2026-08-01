import * as React from 'react';
import { cn } from '@/utils';

export const DashboardGrid = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, children, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn('grid grid-cols-1 gap-6 md:grid-cols-12', className)}
        {...props}
      >
        {children}
      </div>
    );
  }
);
DashboardGrid.displayName = 'DashboardGrid';

export const DashboardGridMain = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, children, ...props }, ref) => (
    <div ref={ref} className={cn('col-span-1 md:col-span-8 lg:col-span-8', className)} {...props}>
      {children}
    </div>
  )
);
DashboardGridMain.displayName = 'DashboardGridMain';

export const DashboardGridSidebar = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, children, ...props }, ref) => (
    <div ref={ref} className={cn('col-span-1 md:col-span-4 lg:col-span-4', className)} {...props}>
      {children}
    </div>
  )
);
DashboardGridSidebar.displayName = 'DashboardGridSidebar';
