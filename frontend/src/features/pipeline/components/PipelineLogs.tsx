import * as React from 'react';
import { LogViewer } from '@/components/pipeline';
import type { UINode } from '../utils';

export const PipelineLogs: React.FC<{ node: UINode }> = ({ node }) => {
  return (
    <div className="space-y-4 fade-in">
      <h3 className="text-sm font-semibold tracking-tight text-muted-foreground uppercase">Agent Output</h3>
      <LogViewer logs={node.logs} />
    </div>
  );
};
