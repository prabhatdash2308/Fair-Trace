import * as React from 'react';
import { useNavigate } from 'react-router-dom';
import { ROUTES } from '@/constants/routes';
import { PrimaryButton } from '@/components/ui/PrimaryButton';
import { Play } from 'lucide-react';
import type { ReviewCycle } from '../../types/review.types';
import { reviewApi } from '../../api/review.api';

export const ReviewPipelineTab: React.FC<{ cycle: ReviewCycle }> = ({ cycle }) => {
  const navigate = useNavigate();
  const [isTriggering, setIsTriggering] = React.useState(false);

  const handleTrigger = async () => {
    setIsTriggering(true);
    try {
      const res = await reviewApi.triggerPipeline(cycle.id);
      navigate(ROUTES.pipelineMonitor(res.pipeline_run_id));
    } catch (err: any) {
      alert('Failed to start pipeline: ' + err.message);
    } finally {
      setIsTriggering(false);
    }
  };

  return (
    <div className="space-y-6 fade-in">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold tracking-tight">AI Pipeline Execution</h3>
        <PrimaryButton onClick={() => navigate(ROUTES.PIPELINE)}>
          View All Pipelines
        </PrimaryButton>
      </div>
      <div className="flex flex-col items-center justify-center p-12 rounded-lg border border-dashed border-border/50 bg-muted/10 text-center">
        <Play className="h-8 w-8 text-muted-foreground mb-4 opacity-50" />
        <p className="text-sm font-medium mb-1">Pipeline has not been executed.</p>
        <p className="text-xs text-muted-foreground mb-6">Trigger the pipeline to begin evidence retrieval and bias detection.</p>
        <PrimaryButton onClick={handleTrigger} disabled={isTriggering}>
          {isTriggering ? 'Starting...' : 'Start AI Analysis'}
        </PrimaryButton>
      </div>
    </div>
  );
};
