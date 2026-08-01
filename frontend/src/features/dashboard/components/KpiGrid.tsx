import * as React from 'react';
import { Briefcase, Activity, CheckCircle2, Clock } from 'lucide-react';
import { StatGrid } from '@/components/layout';
import { MetricCard } from '@/components/cards';
import { useDashboardKPIs } from '../hooks/useDashboard';

export const KpiGrid: React.FC = () => {
  const { data, isLoading } = useDashboardKPIs();

  return (
    <StatGrid>
      <MetricCard
        title="Total Cycles"
        value={data?.totalCycles}
        icon={Briefcase}
        description="All time"
        isLoading={isLoading}
      />
      <MetricCard
        title="Active Cycles"
        value={data?.activeCycles}
        icon={Activity}
        description="Currently running"
        isLoading={isLoading}
      />
      <MetricCard
        title="Pending Approval"
        value={data?.pendingApprovals}
        icon={Clock}
        description="Awaiting review"
        isLoading={isLoading}
      />
      <MetricCard
        title="Completed"
        value={data?.completedThisMonth}
        icon={CheckCircle2}
        description="This month"
        isLoading={isLoading}
      />
    </StatGrid>
  );
};
