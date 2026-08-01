import * as React from 'react';
import type { Report } from '../../types/report.types';
import { Lightbulb } from 'lucide-react';

export const ReportRecommendations: React.FC<{ report: Report }> = ({ report }) => {
  const hasRecommendations = report.recommended_actions && report.recommended_actions.length > 0;

  return (
    <section id="recommendations" className="scroll-mt-24 space-y-4">
      <h2 className="text-2xl font-semibold tracking-tight">AI Recommendations</h2>
      
      {hasRecommendations ? (
        <div className="space-y-3 max-w-4xl">
          {report.recommended_actions?.map((rec, idx) => (
            <div key={idx} className="flex gap-3 p-4 rounded-md border border-border/50 bg-muted/10">
              <Lightbulb className="h-5 w-5 text-primary shrink-0 mt-0.5" />
              <p className="text-sm text-foreground/90">{rec}</p>
            </div>
          ))}
        </div>
      ) : (
        <div className="p-6 rounded-md border border-dashed border-border/50 bg-muted/10 max-w-4xl">
          <p className="text-sm font-medium">No AI recommendations available.</p>
          <p className="text-xs text-muted-foreground mt-1">Generate an AI report from the Review workspace.</p>
        </div>
      )}
    </section>
  );
};
