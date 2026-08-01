import * as React from 'react';
import { cn } from '@/lib/utils';
import { ExecutionNode } from './ExecutionNode';
import type { UINode } from '@/features/pipeline/utils';

export interface ExecutionGraphProps {
  nodes: UINode[];
  onNodeSelect?: (node: UINode) => void;
  selectedNodeId?: string;
  className?: string;
}

export const ExecutionGraph: React.FC<ExecutionGraphProps> = ({
  nodes,
  onNodeSelect,
  selectedNodeId,
  className,
}) => {
  if (!nodes?.length) return null;

  return (
    <div className={cn("flex flex-col gap-4", className)}>
      {nodes.map((node, index) => (
        <ExecutionNode
          key={node.id}
          node={node}
          isLast={index === nodes.length - 1}
          onClick={onNodeSelect}
          isActive={node.id === selectedNodeId}
        />
      ))}
    </div>
  );
};
