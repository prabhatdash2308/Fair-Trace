import * as React from 'react';
import type { Report } from '../../types/report.types';

export const ReportPerformance: React.FC<{ report: Report }> = ({ report }) => {
  const hasClaims = report.claims && report.claims.length > 0;

  return (
    <section id="performance" className="scroll-mt-24 space-y-4">
      <h2 className="text-2xl font-semibold tracking-tight">Competency Breakdown</h2>
      
      {hasClaims ? (
        <div className="space-y-6 max-w-4xl">
          {report.claims.map((claim) => (
            <div key={claim.id} className="pb-6 border-b border-border/30 last:border-0">
              <div className="flex items-center gap-3 mb-2">
                <h3 className="text-lg font-medium">{claim.dimension}</h3>
                <span className="text-xs px-2 py-0.5 rounded-full bg-muted text-muted-foreground">
                  Confidence: {claim.confidence}
                </span>
              </div>
              <p className="text-sm font-medium mb-2">{claim.claim_text}</p>
              <p className="text-sm text-muted-foreground leading-relaxed">{claim.explanation}</p>
            </div>
          ))}
        </div>
      ) : (
        <div className="p-6 rounded-md border border-dashed border-border/50 bg-muted/10 max-w-4xl">
          <p className="text-sm font-medium">No performance data available.</p>
          <p className="text-xs text-muted-foreground mt-1">Generate an AI report from the Review workspace.</p>
        </div>
      )}
    </section>
  );
};
