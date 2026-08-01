import * as React from 'react';
import { ExecutionNode } from '@/components/pipeline';
import type { UINode } from '../utils';

// Re-export or thinly wrap if specifically requested by file structure.
export const PipelineNode: React.FC<{ node: UINode }> = ({ node }) => {
  return <ExecutionNode node={node} />;
};
