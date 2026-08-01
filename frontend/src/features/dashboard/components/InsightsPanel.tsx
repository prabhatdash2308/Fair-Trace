import * as React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Sparkles } from 'lucide-react';

export const InsightsPanel: React.FC = () => {
  // We do not mock AI data per requirements.
  return (
    <Card className="h-full border-border/50 shadow-sm overflow-hidden">
      <CardHeader className="pb-3 border-b border-border/50 bg-muted/20">
        <CardTitle className="text-base font-semibold flex items-center gap-2">
          <Sparkles className="h-4 w-4 text-foreground" />
          AI Insights
        </CardTitle>
      </CardHeader>
      <CardContent className="pt-6">
        <div className="flex h-[200px] flex-col items-center justify-center text-center">
          <div className="mb-2 flex h-10 w-10 items-center justify-center rounded-full bg-muted/50">
            <Sparkles className="h-5 w-5 text-muted-foreground opacity-50" />
          </div>
          <h3 className="text-sm font-medium mb-1">No insights generated</h3>
          <p className="text-sm text-muted-foreground max-w-[200px]">
            AI Insights will appear here after the first completed review cycle.
          </p>
        </div>
      </CardContent>
    </Card>
  );
};
