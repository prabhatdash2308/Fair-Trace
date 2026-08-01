import * as React from 'react';
import type { Report } from '../../types/report.types';

export const ReportEvidence: React.FC<{ report: Report }> = ({ report }) => {
  // Aggregate citations from claims
  const allCitations = report.claims?.flatMap(c => c.citations) || [];

  return (
    <section id="evidence" className="scroll-mt-24 space-y-4">
      <h2 className="text-2xl font-semibold tracking-tight">Supporting Evidence</h2>
      
      {allCitations.length > 0 ? (
        <div className="space-y-4 max-w-4xl">
          {allCitations.map((cit, idx) => (
            <div key={cit.id || idx} className="p-4 rounded-md bg-muted/20 border border-border/50">
              <p className="text-sm italic text-foreground/80">"{cit.extracted_passage}"</p>
              <p className="text-xs text-muted-foreground mt-2">Similarity: {(cit.similarity_score * 100).toFixed(1)}%</p>
            </div>
          ))}
        </div>
      ) : (
        <div className="p-6 rounded-md border border-dashed border-border/50 bg-muted/10 max-w-4xl">
          <p className="text-sm font-medium">No AI evidence available.</p>
          <p className="text-xs text-muted-foreground mt-1">Generate an AI report from the Review workspace to retrieve citations.</p>
        </div>
      )}
    </section>
  );
};
