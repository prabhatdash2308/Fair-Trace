import * as React from 'react';
import { BaseEmptyState } from '@/components/feedback';
import { Activity } from 'lucide-react';

export const PipelineEmpty: React.FC = () => {
  return (
    <BaseEmptyState 
      icon={Activity}
      title="No pipeline executions available"
      description="There are currently no AI pipelines running or historically completed for this context."
    />
  );
};
