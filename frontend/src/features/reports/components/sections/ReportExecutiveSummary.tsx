import * as React from 'react';
import type { Report } from '../../types/report.types';

export const ReportExecutiveSummary: React.FC<{ report: Report }> = ({ report }) => {
  return (
    <section id="overview" className="scroll-mt-24 space-y-4">
      <h2 className="text-2xl font-semibold tracking-tight">Executive Summary</h2>
      
      {report.executive_summary ? (
        <div className="text-base leading-7 text-foreground/90 whitespace-pre-wrap max-w-4xl">
          {report.executive_summary}
        </div>
      ) : (
        <div className="p-6 rounded-md border border-dashed border-border/50 bg-muted/10">
          <p className="text-sm font-medium">No AI analysis available.</p>
          <p className="text-xs text-muted-foreground mt-1">Generate an AI report from the Review workspace to populate this summary.</p>
        </div>
      )}
    </section>
  );
};
