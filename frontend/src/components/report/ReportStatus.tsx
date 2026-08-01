import * as React from 'react';
import { cn } from '@/lib/utils';
import { CheckCircle2, Clock, AlertCircle, FileText } from 'lucide-react';
import type { ReportStatus as BackendReportStatus } from '@/features/reports/types/report.types';

export interface ReportStatusProps {
  status: BackendReportStatus;
  className?: string;
  showIcon?: boolean;
}

export const ReportStatus: React.FC<ReportStatusProps> = ({ status, className, showIcon = true }) => {
  let label = 'Draft';
  let colorClass = 'text-muted-foreground bg-muted border-border/50';
  let Icon = FileText;

  switch (status) {
    case 'PENDING_APPROVAL':
      label = 'Pending Approval';
      colorClass = 'text-warning-foreground bg-warning/20 border-warning/30';
      Icon = Clock;
      break;
    case 'FINALIZED':
      label = 'Approved';
      colorClass = 'text-success bg-success/10 border-success/20';
      Icon = CheckCircle2;
      break;
    case 'REVISION_REQUESTED':
      label = 'Revision Requested';
      colorClass = 'text-blue-500 bg-blue-500/10 border-blue-500/20';
      Icon = AlertCircle;
      break;
    case 'REJECTED':
      label = 'Rejected';
      colorClass = 'text-destructive bg-destructive/10 border-destructive/20';
      Icon = AlertCircle;
      break;
    case 'DRAFT':
    default:
      label = 'Draft';
      colorClass = 'text-muted-foreground bg-muted border-border/50';
      Icon = FileText;
      break;
  }

  return (
    <div className={cn("inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold shadow-sm transition-colors", colorClass, className)}>
      {showIcon && <Icon className="mr-1.5 h-3.5 w-3.5" />}
      {label}
    </div>
  );
};
