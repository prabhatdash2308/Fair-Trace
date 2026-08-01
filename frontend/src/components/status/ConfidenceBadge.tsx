import * as React from 'react';
import { StatusBadge } from './StatusBadge';
import { AIIcons, StatusIcons } from '@/components/icons';

type ConfidenceLevel = 'HIGH' | 'MEDIUM' | 'LOW' | 'INSUFFICIENT';

interface ConfidenceBadgeProps {
  level: ConfidenceLevel;
  className?: string;
  showIcon?: boolean;
}

const config: Record<ConfidenceLevel, { label: string; variant: 'success' | 'warning' | 'danger' | 'muted'; icon: React.ElementType }> = {
  HIGH: { label: 'High Confidence', variant: 'success', icon: AIIcons.Sparkles },
  MEDIUM: { label: 'Medium Confidence', variant: 'warning', icon: StatusIcons.Warning },
  LOW: { label: 'Low Confidence', variant: 'danger', icon: StatusIcons.Critical },
  INSUFFICIENT: { label: 'Insufficient Data', variant: 'muted', icon: StatusIcons.Unknown },
};

export const ConfidenceBadge: React.FC<ConfidenceBadgeProps> = ({ level, className, showIcon = true }) => {
  const conf = config[level];
  if (!conf) return <StatusBadge variant="muted" className={className}>{level}</StatusBadge>;

  return (
    <StatusBadge variant={conf.variant} icon={conf.icon} showIcon={showIcon} className={className}>
      {conf.label}
    </StatusBadge>
  );
};
