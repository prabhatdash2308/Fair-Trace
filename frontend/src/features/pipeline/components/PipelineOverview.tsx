import * as React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { PipelineProgress } from '@/components/pipeline';
import type { UIPipeline } from '../utils';

export const PipelineOverview: React.FC<{ pipeline: UIPipeline }> = ({ pipeline }) => {
  const Icon = pipeline.statusConfig.icon;

  return (
    <Card className="border-border/50 shadow-sm overflow-hidden">
      <CardContent className="p-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-6">
          <div className="flex items-center gap-4">
            <div className={`flex h-12 w-12 items-center justify-center rounded-lg ${pipeline.statusConfig.bg}`}>
              <Icon className={`h-6 w-6 ${pipeline.statusConfig.color} ${pipeline.statusConfig.animation || ''}`} />
            </div>
            <div>
              <h2 className="text-xl font-bold tracking-tight">{pipeline.statusLabel}</h2>
              <p className="text-sm text-muted-foreground mt-1">
                Current Node: <span className="font-medium text-foreground">{pipeline.currentNode}</span>
              </p>
            </div>
          </div>
          <div className="flex items-center gap-6 text-sm">
            <div className="flex flex-col">
              <span className="text-muted-foreground text-xs">Total Duration</span>
              <span className="font-medium">{pipeline.totalLatencyMs} ms</span>
            </div>
            <div className="flex flex-col">
              <span className="text-muted-foreground text-xs">Total Cost</span>
              <span className="font-medium">${pipeline.totalCostUsd.toFixed(4)}</span>
            </div>
            <div className="flex flex-col">
              <span className="text-muted-foreground text-xs">Tokens Used</span>
              <span className="font-medium">{pipeline.totalTokens.toLocaleString()}</span>
            </div>
          </div>
        </div>
        <PipelineProgress 
          progress={pipeline.progress} 
          statusConfig={pipeline.statusConfig} 
          showLabel 
        />
      </CardContent>
    </Card>
  );
};
