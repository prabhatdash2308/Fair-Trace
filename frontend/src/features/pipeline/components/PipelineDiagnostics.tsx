import * as React from 'react';
import { MetricGroup } from '@/components/pipeline';
import { MetricCard } from '@/components/cards';
import { Database, DollarSign, Clock, RotateCcw } from 'lucide-react';
import type { UINode } from '../utils';

export const PipelineDiagnostics: React.FC<{ node: UINode }> = ({ node }) => {
  return (
    <div className="space-y-4 fade-in">
      <h3 className="text-sm font-semibold tracking-tight text-muted-foreground uppercase">Diagnostics</h3>
      <MetricGroup columns={4}>
        <MetricCard
          title="Tokens Used"
          value={node.tokensTotal?.toLocaleString() || '—'}
          icon={Database}
        />
        <MetricCard
          title="Estimated Cost"
          value={node.costUsd ? `$${node.costUsd.toFixed(4)}` : '—'}
          icon={DollarSign}
        />
        <MetricCard
          title="Latency"
          value={node.latencyMs ? `${node.latencyMs} ms` : '—'}
          icon={Clock}
        />
        <MetricCard
          title="Retries"
          value="0" // Optional field not in schema yet.
          icon={RotateCcw}
        />
      </MetricGroup>
    </div>
  );
};
