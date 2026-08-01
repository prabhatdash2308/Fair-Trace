import * as React from 'react';
import { Timeline, type TimelineEvent } from '@/components/timeline';
import { PlayCircle, Clock, CheckCircle2, User, UserCheck } from 'lucide-react';

export const ReviewApprovalTab: React.FC = () => {
  // Mocking the rich workflow timeline per requirements.
  // In a real scenario, this would map over an approval history array from the backend.
  const events: TimelineEvent[] = [
    { id: '1', title: 'Created', date: 'Oct 10, 2023', icon: PlayCircle, isActive: false, description: 'Review cycle drafted.' },
    { id: '2', title: 'Running', date: 'Oct 11, 2023', icon: Clock, isActive: false, description: 'AI processing evidence.' },
    { id: '3', title: 'Waiting for Manager', date: 'Oct 12, 2023', icon: User, isActive: true, description: 'Manager needs to approve AI insights.' },
    { id: '4', title: 'Waiting for HR', date: 'Pending', icon: UserCheck, isActive: false },
    { id: '5', title: 'Approved', date: 'Pending', icon: CheckCircle2, isActive: false },
    { id: '6', title: 'Completed', date: 'Pending', icon: CheckCircle2, isActive: false }
  ];

  return (
    <div className="space-y-6 fade-in">
      <h3 className="text-lg font-semibold tracking-tight">Approval Workflow</h3>
      <div className="p-6 rounded-lg border border-border/50 bg-card">
        <Timeline events={events} />
      </div>
    </div>
  );
};
