import * as React from 'react';
import { cn } from '@/lib/utils';
import { ResponsiveGrid } from '@/components/layout';

export interface MetricGroupProps {
  children: React.ReactNode;
  columns?: 1 | 2 | 3 | 4;
  className?: string;
}

export const MetricGroup: React.FC<MetricGroupProps> = ({ children, columns = 4, className }) => {
  return (
    <ResponsiveGrid columns={columns} className={cn("gap-4", className)}>
      {children}
    </ResponsiveGrid>
  );
};
