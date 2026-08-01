import * as React from 'react';
import { cn } from '@/lib/utils';
import type { StatusConfig } from '@/features/pipeline/constants';

export interface PipelineProgressProps {
  progress: number;
  statusConfig: StatusConfig;
  className?: string;
  showLabel?: boolean;
}

export const PipelineProgress: React.FC<PipelineProgressProps> = ({ 
  progress, 
  statusConfig, 
  className,
  showLabel = false 
}) => {
  // Use a generic primary color for progress if the status isn't error/success
  const bgClass = statusConfig.label === 'Failed' ? 'bg-destructive' : 
                  statusConfig.label === 'Completed' ? 'bg-success' : 'bg-primary';

  return (
    <div className={cn("w-full", className)}>
      {showLabel && (
        <div className="flex justify-between items-center mb-1 text-xs text-muted-foreground">
          <span>{statusConfig.label}</span>
          <span>{progress}%</span>
        </div>
      )}
      <div className="h-1.5 w-full overflow-hidden rounded-full bg-muted">
        <div
          className={cn("h-full rounded-full transition-all duration-500", bgClass)}
          style={{ width: `${Math.max(0, Math.min(100, progress))}%` }}
        />
      </div>
    </div>
  );
};
