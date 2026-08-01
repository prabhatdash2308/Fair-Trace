import * as React from 'react';
import { Timeline, type TimelineEvent } from '@/components/timeline';
import { PlayCircle, CheckCircle2 } from 'lucide-react';
import { formatDate } from '@/utils';
import type { ReviewCycle } from '../../types/review.types';

export const ReviewTimelineTab: React.FC<{ cycle: ReviewCycle }> = ({ cycle }) => {
  const events: TimelineEvent[] = [
    {
      id: 'created',
      title: 'Review Cycle Drafted',
      date: formatDate(cycle.created_at),
      icon: PlayCircle,
      isActive: true,
      description: 'The review cycle was initialized.'
    }
  ];

  if (cycle.status === 'COMPLETED') {
    events.push({
      id: 'completed',
      title: 'Review Completed',
      date: formatDate(cycle.updated_at),
      icon: CheckCircle2,
      isActive: false,
      description: `Review finalized.`
    });
  }

  return (
    <div className="space-y-6 fade-in">
      <h3 className="text-lg font-semibold tracking-tight">Event Timeline</h3>
      <div className="py-4">
        <Timeline events={events} />
      </div>
    </div>
  );
};
