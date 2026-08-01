/**
 * Dashboard feature types.
 * The dashboard is a derived view — it aggregates data from multiple endpoints.
 * No dedicated backend endpoint exists for dashboard data.
 */

import type { ReviewCycleStatus } from '@/features/reviews';
import type { PipelineStatus } from '@/features/pipeline';
import type { ReportStatus } from '@/features/reports';

/** KPI card data shape for the dashboard summary row. */
export interface DashboardKPI {
  totalCycles: number;
  activeCycles: number;
  pendingApprovals: number;
  completedThisMonth: number;
}

/** A single cycle with its active pipeline run for the status panel. */
export interface CyclePipelineSummary {
  cycleId: string;
  cycleTitle: string;
  employeeName: string;
  cycleStatus: ReviewCycleStatus;
  pipelineRunId: string | null;
  pipelineStatus: PipelineStatus | null;
  reportStatus: ReportStatus | null;
}

/** Trend direction for KPI metric cards. */
export type TrendDirection = 'up' | 'down' | 'neutral';

export interface KPITrend {
  direction: TrendDirection;
  value: number;
  label: string;
}
