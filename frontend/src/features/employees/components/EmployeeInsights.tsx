import * as React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Sparkles } from 'lucide-react';

export const EmployeeInsights: React.FC = () => {
  return (
    <div className="space-y-6 fade-in">
      <h3 className="text-lg font-semibold tracking-tight">AI Insights</h3>
      <Card className="border-border/50 shadow-sm bg-muted/20">
        <CardContent className="flex flex-col items-center justify-center p-12 text-center">
          <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-muted shadow-sm">
            <Sparkles className="h-6 w-6 text-muted-foreground" />
          </div>
          <h4 className="text-base font-semibold">No AI Insights Available</h4>
          <p className="mt-2 max-w-sm text-sm text-muted-foreground">
            AI analysis requires a completed review cycle with processed documents. 
            Insights will appear here once the pipeline finishes processing.
          </p>
        </CardContent>
      </Card>
    </div>
  );
};
