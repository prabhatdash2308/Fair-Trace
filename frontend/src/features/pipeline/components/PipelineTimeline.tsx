import * as React from 'react';
import { Timeline, type TimelineEvent } from '@/components/timeline';
import { PlayCircle, CheckCircle2 } from 'lucide-react';
import { formatDate } from '@/utils';
import type { UIPipeline } from '../utils';

export const PipelineTimeline: React.FC<{ pipeline: UIPipeline }> = ({ pipeline }) => {
  const events: TimelineEvent[] = [
    {
      id: 'started',
      title: 'Pipeline Triggered',
      date: formatDate(pipeline.startedAt),
      icon: PlayCircle,
      isActive: true,
      description: 'The AI analysis pipeline was initialized.'
    }
  ];

  if (pipeline.completedAt) {
    events.push({
      id: 'completed',
      title: 'Pipeline Completed',
      date: formatDate(pipeline.completedAt),
      icon: CheckCircle2,
      isActive: false,
      description: `Finished execution in ${pipeline.totalLatencyMs}ms.`
    });
  }

  return (
    <div className="space-y-4 fade-in">
      <h3 className="text-sm font-semibold tracking-tight text-muted-foreground uppercase">Event Timeline</h3>
      <div className="py-4">
        <Timeline events={events} />
      </div>
    </div>
  );
};
