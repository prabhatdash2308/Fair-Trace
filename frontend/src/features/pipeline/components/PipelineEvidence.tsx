import * as React from 'react';
import type { UINode } from '../utils';

export const PipelineEvidence: React.FC<{ node: UINode }> = ({ node }) => {
  return (
    <div className="space-y-4 fade-in">
      <h3 className="text-sm font-semibold tracking-tight text-muted-foreground uppercase">Evidence & Findings</h3>
      <div className="flex h-32 w-full flex-col items-center justify-center rounded-md border border-dashed border-border/50 bg-muted/20 text-center">
        <p className="text-sm text-muted-foreground">
          {node.normalizedStatus === 'COMPLETED' 
            ? 'No evidence retrieved for this stage.' 
            : 'Evidence will appear after analysis completes.'}
        </p>
      </div>
    </div>
  );
};
