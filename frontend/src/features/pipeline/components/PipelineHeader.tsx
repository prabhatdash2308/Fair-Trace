import * as React from 'react';
import { PageToolbar } from '@/components/layout';
import { PrimaryButton } from '@/components/ui/PrimaryButton';
import { Play } from 'lucide-react';
import type { UIPipeline } from '../utils';

export const PipelineHeader: React.FC<{ pipeline: UIPipeline }> = ({ pipeline }) => {
  const isRunning = pipeline.statusLabel === 'Running';

  return (
    <PageToolbar
      title={`Pipeline Run ${pipeline.runId.substring(0, 8)}`}
      description={`Started on ${new Date(pipeline.startedAt).toLocaleString()}`}
      actions={
        <PrimaryButton disabled={isRunning}>
          <Play className="mr-2 h-4 w-4" />
          {isRunning ? 'Running...' : 'Re-run Pipeline'}
        </PrimaryButton>
      }
      className="mb-6"
    />
  );
};
