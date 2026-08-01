import * as React from 'react';
import { Timeline, type TimelineEvent } from '@/components/timeline';
import { UserPlus } from 'lucide-react';
import { formatDate } from '@/utils';
import type { Employee } from '../types';

export const EmployeeTimeline: React.FC<{ employee: Employee }> = ({ employee }) => {
  const events: TimelineEvent[] = [
    {
      id: 'joined',
      title: 'Joined Company',
      date: formatDate(employee.created_at),
      icon: UserPlus,
      isActive: true,
      description: 'Employee profile was created in the system.'
    }
    // Cannot mock AI or Review events per constraints, so just show Joined.
  ];

  return (
    <div className="space-y-6 fade-in">
      <h3 className="text-lg font-semibold tracking-tight">Timeline</h3>
      <div className="py-4">
        <Timeline events={events} />
      </div>
    </div>
  );
};
