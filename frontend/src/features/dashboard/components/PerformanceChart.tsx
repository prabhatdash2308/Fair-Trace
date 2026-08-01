import * as React from 'react';
import { LineChartCard } from '@/components/charts';

export const PerformanceChart: React.FC = () => {
  // Empty data gracefully falls back to empty state.
  return (
    <LineChartCard
      title="Performance Trends"
      description="Company-wide performance scores over time."
      data={[]}
      xAxisKey="month"
      seriesKeys={[
        { key: 'score', name: 'Average Score', color: 'hsl(var(--foreground))' },
      ]}
      isEmpty={true}
      emptyMessage="Not enough historical data to generate performance trends."
      className="shadow-sm border-border/50"
    />
  );
};
