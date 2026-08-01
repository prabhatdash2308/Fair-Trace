import * as React from 'react';
import { ExecutionGraph } from '@/components/pipeline';
import type { UIPipeline, UINode } from '../utils';

export interface PipelineGraphProps {
  pipeline: UIPipeline;
  selectedNodeId?: string;
  onNodeSelect?: (node: UINode) => void;
}

export const PipelineGraph: React.FC<PipelineGraphProps> = ({ pipeline, selectedNodeId, onNodeSelect }) => {
  return (
    <div className="space-y-4 fade-in">
      <h3 className="text-sm font-semibold tracking-tight text-muted-foreground uppercase">Execution Flow</h3>
      <ExecutionGraph 
        nodes={pipeline.nodes} 
        selectedNodeId={selectedNodeId} 
        onNodeSelect={onNodeSelect} 
      />
    </div>
  );
};
