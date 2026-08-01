import * as React from 'react';
import { cn } from '@/lib/utils';

export interface ReportVersionBadgeProps {
  version: number;
  isCurrent?: boolean;
  className?: string;
}

export const ReportVersionBadge: React.FC<ReportVersionBadgeProps> = ({ version, isCurrent = false, className }) => {
  return (
    <div className={cn(
      "inline-flex items-center rounded-md border px-2 py-0.5 text-xs font-mono font-medium",
      isCurrent ? "bg-primary/10 text-primary border-primary/20" : "bg-muted text-muted-foreground border-border/50",
      className
    )}>
      v{version}.0
    </div>
  );
};
