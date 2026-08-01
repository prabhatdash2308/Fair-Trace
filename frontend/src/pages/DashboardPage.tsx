import * as React from 'react';
import { motion } from 'framer-motion';
import { pageTransition } from '@/components/motion';
import { DashboardGrid, DashboardGridMain, DashboardGridSidebar } from '@/components/layout';

import {
  DashboardHeader,
  KpiGrid,
  PipelineOverview,
  ReviewQueue,
  ActivityFeed,
  InsightsPanel,
  PerformanceChart,
  ApprovalQueue,
} from '@/features/dashboard/components';

export default function DashboardPage() {
  return (
    <motion.div
      variants={pageTransition}
      initial="hidden"
      animate="visible"
      exit="exit"
      className="flex flex-col gap-6 pb-12"
    >
      {/* 1. Header & Primary Action */}
      <DashboardHeader />

      {/* 2. Quick Metrics */}
      <KpiGrid />

      {/* 3. Main Dashboard Layout (Grid) */}
      <DashboardGrid>
        
        {/* Main Column */}
        <DashboardGridMain className="flex flex-col gap-6">
          <PipelineOverview />
          <ReviewQueue />
          <PerformanceChart />
        </DashboardGridMain>
        
        {/* Sidebar Column */}
        <DashboardGridSidebar className="flex flex-col gap-6">
          <InsightsPanel />
          <ActivityFeed />
          <ApprovalQueue />
        </DashboardGridSidebar>
        
      </DashboardGrid>
    </motion.div>
  );
}
