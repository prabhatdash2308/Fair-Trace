import * as React from 'react';
import { cn } from '@/lib/utils';
import { formatDate } from '@/utils';
import { AlertCircle, CheckCircle2 } from 'lucide-react';
import type { ConfidenceLevel } from '@/features/reports/types/report.types';

export interface DecisionHeroProps {
  decision: string;
  confidence: ConfidenceLevel | null;
  generatedAt: string;
  reportId: string;
  pipelineId: string;
}

export const DecisionHero: React.FC<DecisionHeroProps> = ({ 
  decision, 
  confidence, 
  generatedAt,
  reportId,
  pipelineId
}) => {
  let confidenceColor = "text-muted-foreground";
  if (confidence === 'HIGH') confidenceColor = "text-success";
  if (confidence === 'MEDIUM') confidenceColor = "text-primary";
  if (confidence === 'LOW') confidenceColor = "text-warning-foreground";
  if (confidence === 'INSUFFICIENT') confidenceColor = "text-destructive";

  return (
    <div className="flex flex-col gap-6 pb-12 pt-4">
      <div className="flex items-center gap-2 text-sm font-medium text-muted-foreground uppercase tracking-wider">
        <CheckCircle2 className="h-4 w-4" /> AI Decision
      </div>
      
      <h1 className="text-4xl md:text-5xl font-bold tracking-tight text-foreground">
        {decision || "Analysis Pending"}
      </h1>
      
      <div className="flex flex-wrap items-center gap-x-6 gap-y-4 text-sm font-medium">
        {confidence ? (
          <span className={cn("inline-flex items-center gap-1.5", confidenceColor)}>
            <div className="h-2 w-2 rounded-full bg-current" />
            {confidence} Confidence
          </span>
        ) : (
          <span className="inline-flex items-center gap-1.5 text-muted-foreground">
            <AlertCircle className="h-3.5 w-3.5" />
            Confidence Unavailable
          </span>
        )}
        
        <span className="text-muted-foreground">Generated {formatDate(generatedAt)}</span>
        <span className="text-muted-foreground">Report #{reportId.substring(0, 6)}</span>
        <span className="text-muted-foreground">Pipeline #{pipelineId.substring(0, 6)}</span>
      </div>
    </div>
  );
};
