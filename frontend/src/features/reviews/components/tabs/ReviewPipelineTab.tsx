import * as React from 'react';
import { useNavigate } from 'react-router-dom';
import { ROUTES } from '@/constants/routes';
import { PrimaryButton } from '@/components/ui/PrimaryButton';
import { Play } from 'lucide-react';
import type { ReviewCycle } from '../../types/review.types';

export const ReviewPipelineTab: React.FC<{ cycle: ReviewCycle }> = ({ cycle }) => {
  const navigate = useNavigate();

  return (
    <div className="space-y-6 fade-in">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold tracking-tight">AI Pipeline Execution</h3>
        <PrimaryButton onClick={() => navigate(ROUTES.pipelineMonitor(cycle.id))}>
          View Detailed Pipeline
        </PrimaryButton>
      </div>
      <div className="flex flex-col items-center justify-center p-12 rounded-lg border border-dashed border-border/50 bg-muted/10 text-center">
        <Play className="h-8 w-8 text-muted-foreground mb-4 opacity-50" />
        <p className="text-sm font-medium mb-1">Pipeline has not been executed.</p>
        <p className="text-xs text-muted-foreground">Trigger the pipeline to begin evidence retrieval and bias detection.</p>
      </div>
    </div>
  );
};
