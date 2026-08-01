import * as React from 'react';

export const ReviewScores: React.FC = () => {
  return (
    <div className="space-y-6 fade-in">
      <h3 className="text-lg font-semibold tracking-tight">AI Generated Scores & Insights</h3>
      <div className="flex flex-col items-center justify-center p-12 rounded-lg border border-dashed border-border/50 bg-muted/10 text-center">
        <p className="text-sm font-medium mb-1">No AI analysis has been generated for this review yet.</p>
        <p className="text-xs text-muted-foreground">Start the AI Pipeline to generate analysis, scores, and confidence metrics.</p>
      </div>
    </div>
  );
};
