import * as React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { pageTransition } from '@/components/motion';
import { IconButton } from '@/components/ui/IconButton';
import { ArrowLeft, Loader2 } from 'lucide-react';
import { ROUTES } from '@/constants/routes';
import { useReport, useReportVersions } from '@/features/reports/hooks/useReports';

import {
  ReportMetadata,
  ReportExecutiveSummary,
  ReportPerformance,
  ReportEvidence,
  ReportBias,
  ReportRecommendations,
  ReportLimitations,
  ReportApprovalStatus,
  ReportVersions
} from '@/features/reports/components/sections';

export default function ReportDetailsPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const { data: report, isLoading } = useReport(id || '');
  const { data: versions } = useReportVersions(id || '');

  // Progressive loading states
  const [showContent, setShowContent] = React.useState(false);

  React.useEffect(() => {
    if (report && !isLoading) {
      // Simulate progressive loading of sections after metadata
      const timer = setTimeout(() => setShowContent(true), 150);
      return () => clearTimeout(timer);
    }
  }, [report, isLoading]);

  if (isLoading) {
    return (
      <div className="flex h-[80vh] items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
      </div>
    );
  }

  if (!report) {
    return (
      <div className="flex flex-col items-center justify-center h-[80vh] text-center">
        <h2 className="text-lg font-semibold">Report Not Found</h2>
        <p className="text-muted-foreground mt-2 mb-4">This report does not exist or has not been generated.</p>
        <button className="btn btn-secondary" onClick={() => navigate(ROUTES.REPORTS)}>Back to Reports</button>
      </div>
    );
  }

  return (
    <motion.div
      variants={pageTransition}
      initial="hidden"
      animate="visible"
      exit="exit"
      className="flex flex-col gap-6 pb-24 w-full max-w-7xl mx-auto"
    >
      <div className="flex items-center gap-2 -mb-2">
        <IconButton icon={ArrowLeft} variant="ghost" onClick={() => navigate(ROUTES.REPORTS)} />
        <span className="text-sm font-medium text-muted-foreground">Back to Reports</span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-[200px_1fr] lg:grid-cols-[240px_1fr] gap-12 mt-4 items-start">
        {/* Sticky Table of Contents (Notion style) */}
        <aside className="sticky top-24 hidden md:flex flex-col gap-2 border-l border-border/50 pl-4 py-2">
          <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2">Contents</span>
          <a href="#overview" className="text-sm text-foreground/70 hover:text-foreground hover:underline transition-colors py-1">Executive Summary</a>
          <a href="#performance" className="text-sm text-foreground/70 hover:text-foreground hover:underline transition-colors py-1">Competency Scores</a>
          <a href="#evidence" className="text-sm text-foreground/70 hover:text-foreground hover:underline transition-colors py-1">Evidence</a>
          <a href="#bias" className="text-sm text-foreground/70 hover:text-foreground hover:underline transition-colors py-1">Bias Analysis</a>
          <a href="#recommendations" className="text-sm text-foreground/70 hover:text-foreground hover:underline transition-colors py-1">Recommendations</a>
          <a href="#limitations" className="text-sm text-foreground/70 hover:text-foreground hover:underline transition-colors py-1">Limitations</a>
          <a href="#approval" className="text-sm text-foreground/70 hover:text-foreground hover:underline transition-colors py-1">Approval Status</a>
          <a href="#versions" className="text-sm text-foreground/70 hover:text-foreground hover:underline transition-colors py-1">Version History</a>
        </aside>

        {/* Document Content */}
        <div className="flex flex-col gap-12 max-w-4xl w-full">
          <ReportMetadata report={report} />
          
          {showContent ? (
            <div className="flex flex-col gap-16 fade-in">
              <ReportExecutiveSummary report={report} />
              <ReportPerformance report={report} />
              <ReportEvidence report={report} />
              <ReportBias report={report} />
              <ReportRecommendations report={report} />
              <ReportLimitations report={report} />
              <ReportApprovalStatus report={report} />
              <ReportVersions versions={versions || []} />
            </div>
          ) : (
            <div className="flex h-48 items-center justify-center fade-in">
              <Loader2 className="h-6 w-6 animate-spin text-muted-foreground/50" />
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
}
