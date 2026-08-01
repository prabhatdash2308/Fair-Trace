import * as React from 'react';
import { StatusBadge } from './StatusBadge';
import { StatusIcons } from '@/components/icons';

type ApprovalStatusType = 'PENDING' | 'APPROVED' | 'REVISION_REQUESTED' | 'REJECTED';

interface ApprovalStatusProps {
  status: ApprovalStatusType;
  className?: string;
  showIcon?: boolean;
}

const config: Record<ApprovalStatusType, { label: string; variant: 'warning' | 'success' | 'default' | 'danger'; icon: React.ElementType }> = {
  PENDING: { label: 'Pending Approval', variant: 'warning', icon: StatusIcons.Pending },
  APPROVED: { label: 'Approved', variant: 'success', icon: StatusIcons.Success },
  REVISION_REQUESTED: { label: 'Revision Required', variant: 'default', icon: StatusIcons.Info },
  REJECTED: { label: 'Rejected', variant: 'danger', icon: StatusIcons.Error },
};

export const ApprovalStatus: React.FC<ApprovalStatusProps> = ({ status, className, showIcon = true }) => {
  const conf = config[status];
  if (!conf) return <StatusBadge variant="muted" className={className}>{status}</StatusBadge>;

  return (
    <StatusBadge variant={conf.variant} icon={conf.icon} showIcon={showIcon} className={className}>
      {conf.label}
    </StatusBadge>
  );
};
