import * as React from 'react';
import type { Report } from '../../types/report.types';

export const ReportLimitations: React.FC<{ report: Report }> = ({ report }) => {
  return (
    <section id="limitations" className="scroll-mt-24 space-y-4">
      <h2 className="text-2xl font-semibold tracking-tight">Confidence & Limitations</h2>
      
      {report.confidence_score ? (
        <div className="p-6 rounded-md border border-border/50 bg-card max-w-4xl space-y-4">
          <div className="flex items-center gap-4">
            <span className="text-sm font-medium text-muted-foreground uppercase tracking-wider">Overall Confidence</span>
            <span className="inline-flex items-center rounded-md border bg-muted px-2.5 py-0.5 text-xs font-semibold">
              {report.confidence_score}
            </span>
          </div>
          <p className="text-sm text-foreground/80 leading-relaxed">
            {report.confidence_explanation || "No further explanation provided by AI."}
          </p>
        </div>
      ) : (
        <div className="p-6 rounded-md border border-dashed border-border/50 bg-muted/10 max-w-4xl">
          <p className="text-sm font-medium">No AI confidence analysis available.</p>
          <p className="text-xs text-muted-foreground mt-1">Generate an AI report from the Review workspace.</p>
        </div>
      )}
    </section>
  );
};
