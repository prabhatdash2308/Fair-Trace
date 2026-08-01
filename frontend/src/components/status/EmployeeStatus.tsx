import * as React from 'react';
import { StatusBadge } from './StatusBadge';
import { StatusIcons } from '@/components/icons';

interface EmployeeStatusProps {
  isActive: boolean;
  className?: string;
  showIcon?: boolean;
}

export const EmployeeStatus: React.FC<EmployeeStatusProps> = ({ isActive, className, showIcon = true }) => {
  return (
    <StatusBadge
      variant={isActive ? 'success' : 'muted'}
      icon={isActive ? StatusIcons.Success : StatusIcons.Error}
      showIcon={showIcon}
      className={className}
    >
      {isActive ? 'Active' : 'Inactive'}
    </StatusBadge>
  );
};
