import * as React from 'react';
import type { ReviewCycle } from '../../types/review.types';

export const ReviewOverview: React.FC<{ cycle: ReviewCycle }> = ({ cycle }) => {
  return (
    <div className="space-y-6 fade-in">
      <h3 className="text-lg font-semibold tracking-tight">Review Overview</h3>
      <div className="p-6 rounded-lg border border-border/50 bg-muted/10">
        <p className="text-sm text-muted-foreground leading-relaxed">
          This review cycle evaluates performance from {cycle.review_period_start} to {cycle.review_period_end}. 
          It encompasses goals, peer feedback, self-assessments, and manager evaluations.
        </p>
      </div>
      {/* Invisible storage for deep linking future-proofing per requirement */}
      <div className="hidden" data-review-id={cycle.id} data-employee-id={cycle.employee_id} data-cycle-id={cycle.id}></div>
    </div>
  );
};
