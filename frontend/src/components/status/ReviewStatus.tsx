import * as React from 'react';
import { StatusBadge } from './StatusBadge';
import { StatusIcons } from '@/components/icons';

type ReviewCycleStatusType = 'DRAFT' | 'ACTIVE' | 'PROCESSING' | 'PENDING_APPROVAL' | 'COMPLETED' | 'CANCELLED';

interface ReviewStatusProps {
  status: ReviewCycleStatusType;
  className?: string;
  showIcon?: boolean;
}

const config: Record<ReviewCycleStatusType, { label: string; variant: 'muted' | 'default' | 'warning' | 'success' | 'secondary'; icon: React.ElementType }> = {
  DRAFT: { label: 'Draft', variant: 'muted', icon: StatusIcons.Info },
  ACTIVE: { label: 'Active', variant: 'default', icon: StatusIcons.Info },
  PROCESSING: { label: 'Processing', variant: 'warning', icon: StatusIcons.Pending },
  PENDING_APPROVAL: { label: 'Pending Approval', variant: 'warning', icon: StatusIcons.Pending },
  COMPLETED: { label: 'Completed', variant: 'success', icon: StatusIcons.Success },
  CANCELLED: { label: 'Cancelled', variant: 'secondary', icon: StatusIcons.Error },
};

export const ReviewStatus: React.FC<ReviewStatusProps> = ({ status, className, showIcon = true }) => {
  const conf = config[status];
  if (!conf) return <StatusBadge variant="muted" className={className}>{status}</StatusBadge>;

  return (
    <StatusBadge variant={conf.variant} icon={conf.icon} showIcon={showIcon} className={className}>
      {conf.label}
    </StatusBadge>
  );
};
