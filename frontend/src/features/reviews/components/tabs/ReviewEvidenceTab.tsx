import * as React from 'react';

export const ReviewEvidenceTab: React.FC = () => {
  return (
    <div className="space-y-6 fade-in">
      <h3 className="text-lg font-semibold tracking-tight">AI Retrieved Evidence</h3>
      <div className="flex flex-col items-center justify-center p-12 rounded-lg border border-dashed border-border/50 bg-muted/10 text-center">
        <p className="text-sm font-medium mb-1">No AI evidence has been retrieved for this review yet.</p>
        <p className="text-xs text-muted-foreground">Start the AI Pipeline to retrieve citations and supporting evidence from documents.</p>
      </div>
    </div>
  );
};
