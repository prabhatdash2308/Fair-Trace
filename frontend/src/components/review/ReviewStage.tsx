import * as React from 'react';
import { cn } from '@/lib/utils';
import { CheckCircle2, Clock, AlertCircle } from 'lucide-react';
import type { ReviewCycleStatus } from '@/features/reviews/types/review.types';

export interface ReviewStageProps {
  status: ReviewCycleStatus;
  className?: string;
  showIcon?: boolean;
}

export const ReviewStage: React.FC<ReviewStageProps> = ({ status, className, showIcon = true }) => {
  let label = 'Draft';
  let colorClass = 'text-muted-foreground bg-muted border-border/50';
  let Icon = Clock;

  switch (status) {
    case 'ACTIVE':
      label = 'Active';
      colorClass = 'text-primary bg-primary/10 border-primary/20';
      Icon = Clock;
      break;
    case 'PROCESSING':
      label = 'AI Processing';
      colorClass = 'text-blue-500 bg-blue-500/10 border-blue-500/20';
      Icon = Clock;
      break;
    case 'PENDING_APPROVAL':
      label = 'Pending Approval';
      colorClass = 'text-warning-foreground bg-warning/20 border-warning/30';
      Icon = AlertCircle;
      break;
    case 'COMPLETED':
      label = 'Completed';
      colorClass = 'text-success bg-success/10 border-success/20';
      Icon = CheckCircle2;
      break;
    case 'CANCELLED':
      label = 'Cancelled';
      colorClass = 'text-destructive bg-destructive/10 border-destructive/20';
      Icon = AlertCircle;
      break;
  }

  return (
    <div className={cn("inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold shadow-sm transition-colors", colorClass, className)}>
      {showIcon && <Icon className="mr-1.5 h-3.5 w-3.5" />}
      {label}
    </div>
  );
};
