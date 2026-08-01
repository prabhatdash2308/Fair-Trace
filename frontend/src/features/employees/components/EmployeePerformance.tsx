import * as React from 'react';
import { LineChartCard, BarChartCard } from '@/components/charts';
import { ResponsiveGrid } from '@/components/layout';

export const EmployeePerformance: React.FC = () => {
  // Empty data for now to avoid faking metrics. 
  // Will gracefully fall back to empty state.
  return (
    <div className="space-y-6 fade-in">
      <h3 className="text-lg font-semibold tracking-tight">Performance History</h3>
      <ResponsiveGrid columns={2}>
        <LineChartCard
          title="Overall Performance Trend"
          description="Scores over the past review cycles"
          data={[]}
          xAxisKey="cycle"
          seriesKeys={[{ key: 'score', name: 'Score' }]}
          isEmpty={true}
          emptyMessage="No historical performance data available."
        />
        <BarChartCard
          title="Competencies"
          description="Latest evaluation breakdown"
          data={[]}
          xAxisKey="competency"
          seriesKeys={[{ key: 'rating', name: 'Rating' }]}
          isEmpty={true}
          emptyMessage="No competency data available."
        />
      </ResponsiveGrid>
    </div>
  );
};
