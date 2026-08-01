import * as React from 'react';
import { cn } from '@/lib/utils';

export interface ScoreBadgeProps {
  score: number | string | null;
  maxScore?: number;
  label?: string;
  className?: string;
}

export const ScoreBadge: React.FC<ScoreBadgeProps> = ({ score, maxScore = 5, label, className }) => {
  if (score === null || score === undefined) {
    return (
      <div className={cn("inline-flex items-center rounded-md border border-border/50 bg-muted/20 px-2.5 py-0.5 text-xs font-semibold text-muted-foreground", className)}>
        {label ? `${label}: ` : ''} Pending
      </div>
    );
  }

  const numericScore = typeof score === 'string' ? parseFloat(score) : score;
  const isNumeric = !isNaN(numericScore);
  
  // Semantic coloring based on score if numeric
  let colorClass = "bg-primary/10 text-primary border-primary/20";
  if (isNumeric) {
    const percentage = numericScore / maxScore;
    if (percentage >= 0.8) colorClass = "bg-success/10 text-success border-success/20";
    else if (percentage < 0.5) colorClass = "bg-destructive/10 text-destructive border-destructive/20";
    else colorClass = "bg-warning/10 text-warning-foreground border-warning/20";
  }

  return (
    <div className={cn("inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-semibold", colorClass, className)}>
      {label && <span className="mr-1 opacity-70">{label}:</span>}
      {score}{isNumeric && maxScore ? `/${maxScore}` : ''}
    </div>
  );
};
