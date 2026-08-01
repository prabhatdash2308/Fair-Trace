import * as React from 'react';
import { StatusBadge } from './StatusBadge';
import { StatusIcons } from '@/components/icons';

type PipelineStatusType = 'QUEUED' | 'RUNNING' | 'COMPLETED' | 'FAILED' | 'HALTED';

interface PipelineStatusProps {
  status: PipelineStatusType;
  className?: string;
  showIcon?: boolean;
}

const config: Record<PipelineStatusType, { label: string; variant: 'muted' | 'default' | 'success' | 'danger' | 'warning'; icon: React.ElementType }> = {
  QUEUED: { label: 'Queued', variant: 'muted', icon: StatusIcons.Pending },
  RUNNING: { label: 'Running', variant: 'default', icon: StatusIcons.Info },
  COMPLETED: { label: 'Completed', variant: 'success', icon: StatusIcons.Success },
  FAILED: { label: 'Failed', variant: 'danger', icon: StatusIcons.Error },
  HALTED: { label: 'Halted', variant: 'warning', icon: StatusIcons.Warning },
};

export const PipelineStatus: React.FC<PipelineStatusProps> = ({ status, className, showIcon = true }) => {
  const conf = config[status];
  if (!conf) return <StatusBadge variant="muted" className={className}>{status}</StatusBadge>;

  return (
    <StatusBadge variant={conf.variant} icon={conf.icon} showIcon={showIcon} className={className}>
      {conf.label}
    </StatusBadge>
  );
};
