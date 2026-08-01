import { cn } from '@/lib/utils';
import type { ReactNode } from 'react';

interface DashboardContainerProps {
  children: ReactNode;
  className?: string;
  /** Number of columns for the metric card grid. Default: 4 */
  cols?: 1 | 2 | 3 | 4;
}

const GRID_COLS = {
  1: 'grid-cols-1',
  2: 'grid-cols-1 sm:grid-cols-2',
  3: 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3',
  4: 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-4',
};

/**
 * DashboardContainer — responsive grid wrapper for metric cards.
 * Used at the top of dashboard pages for the KPI row.
 */
export function DashboardContainer({ children, className, cols = 4 }: DashboardContainerProps) {
  return (
    <div className={cn('grid gap-4', GRID_COLS[cols], className)}>
      {children}
    </div>
  );
}
