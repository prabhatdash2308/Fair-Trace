import * as React from 'react';
import { MetricCard } from '@/components/cards';
import { StatGrid } from '@/components/layout';
import { Calendar, Briefcase, Mail, Activity } from 'lucide-react';
import { formatDate } from '@/utils';
import type { Employee } from '../types';

export const EmployeeOverview: React.FC<{ employee: Employee }> = ({ employee }) => {
  return (
    <div className="space-y-6 fade-in">
      <h3 className="text-lg font-semibold tracking-tight">Overview</h3>
      <StatGrid>
        <MetricCard
          title="Role & Designation"
          value={employee.designation || 'Team Member'}
          icon={Briefcase}
          description={`${employee.department || 'General'} Department`}
        />
        <MetricCard
          title="Contact"
          value={employee.email.split('@')[0]}
          icon={Mail}
          description={employee.email}
        />
        <MetricCard
          title="Joined Date"
          value={formatDate(employee.created_at)}
          icon={Calendar}
          description="Tenure"
        />
        <MetricCard
          title="Current Status"
          value={employee.is_active ? 'Active' : 'Inactive'}
          icon={Activity}
          description="System Access"
        />
      </StatGrid>
    </div>
  );
};
