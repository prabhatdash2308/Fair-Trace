import * as React from 'react';
import { motion } from 'framer-motion';
import { pageTransition } from '@/components/motion';
import { ReportsHeader, ReportsTable } from '@/features/reports/components';

export default function ReportsPage() {
  // TODO: Replace with useReportsList() when the backend endpoint GET /reports is implemented
  const data: any[] = [];
  const isLoading = false;

  return (
    <motion.div
      variants={pageTransition}
      initial="hidden"
      animate="visible"
      exit="exit"
      className="flex flex-col gap-2 pb-12 w-full max-w-7xl mx-auto"
    >
      <ReportsHeader />
      
      <div className="bg-card border border-border/50 rounded-xl overflow-hidden shadow-sm">
        <ReportsTable data={data} isLoading={isLoading} />
      </div>
    </motion.div>
  );
}
