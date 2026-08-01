import * as React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { PipelineStatus } from '@/components/status';
import { Activity } from 'lucide-react';
import { EmptyPipeline } from '@/components/feedback';

export const PipelineOverview: React.FC = () => {
  // In Phase 4, there's no backend endpoint providing global pipeline status metrics yet.
  // We strictly adhere to "DO NOT mock backend data" and show an empty state.
  return (
    <Card className="h-full border-border/50 shadow-sm">
      <CardHeader className="pb-3 border-b border-border/50">
        <div className="flex items-center justify-between">
          <CardTitle className="text-base font-semibold flex items-center gap-2">
            <Activity className="h-4 w-4 text-muted-foreground" />
            Pipeline Overview
          </CardTitle>
          <PipelineStatus status="QUEUED" />
        </div>
      </CardHeader>
      <CardContent className="pt-6">
        <EmptyPipeline 
          description="Pipeline metrics will appear here once the first analysis batch completes." 
        />
      </CardContent>
    </Card>
  );
};
