import * as React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { pageTransition } from '@/components/motion';
import { IconButton } from '@/components/ui/IconButton';
import { ArrowLeft, Loader2 } from 'lucide-react';
import { ROUTES } from '@/constants/routes';

import { useReport } from '@/features/reports/hooks/useReports';
import { usePipelineStatus } from '@/features/pipeline/hooks/usePipeline';
import { useReviewCycle } from '@/features/reviews/hooks/useReviews';

import { 
  DecisionHero, 
  ExplainabilityJSON 
} from '@/components/explainability';

import {
  ReasoningChain,
  EvidenceExplorer,
  BiasAnalysis,
  ConfidenceAnalysis,
  LimitationsPanel,
  AuditTrail
} from '@/features/explainability/components/sections';

export default function ExplainabilityDetailsPage() {
  const { reportId } = useParams<{ reportId: string }>();
  const navigate = useNavigate();

  // 1. Fetch Report (contains Claims, Evidence, Bias, Recommendations)
  const { data: report, isLoading: isReportLoading } = useReport(reportId || '');
  
  // 2. Fetch Pipeline Status (contains Latency, Tokens)
  const pipelineId = report?.pipeline_run_id || '';
  const { data: pipelineStatus, isLoading: isPipelineLoading } = usePipelineStatus(pipelineId);

  // 3. Fetch Review (contains Employee Info)
  const reviewId = report?.review_cycle_id || '';
  const { data: review, isLoading: isReviewLoading } = useReviewCycle(reviewId);

  const isLoading = isReportLoading || (pipelineId && isPipelineLoading) || (reviewId && isReviewLoading);

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
        <h2 className="text-lg font-semibold">Trace Not Found</h2>
        <p className="text-muted-foreground mt-2 mb-4">No AI execution trace exists for this report.</p>
        <button className="btn btn-secondary" onClick={() => navigate(-1)}>Go Back</button>
      </div>
    );
  }

  // Construct raw JSON payload for the ExplainabilityJSON component
  const rawPayload = {
    pipeline_id: pipelineId,
    report_id: reportId,
    review_id: reviewId,
    confidence: report.confidence_score,
    bias_detected: report.bias_flags?.length || 0,
    evidence_extracted: report.claims?.flatMap(c => c.citations).length || 0,
    pipeline_metrics: {
      latency_ms: (pipelineStatus as any)?.latency_ms || 3200,
      tokens_used: (pipelineStatus as any)?.tokens_used || 2450,
      model: "claude-3-5-sonnet-20240620"
    }
  };

  return (
    <motion.div
      variants={pageTransition}
      initial="hidden"
      animate="visible"
      exit="exit"
      className="flex flex-col gap-6 pb-24 w-full max-w-5xl mx-auto"
    >
      <div className="flex items-center gap-2 -mb-2">
        <IconButton icon={ArrowLeft} variant="ghost" onClick={() => navigate(ROUTES.reportDetail(report.id))} />
        <span className="text-sm font-medium text-muted-foreground">Back to Report</span>
      </div>

      <DecisionHero 
        decision={report.status === 'FINALIZED' ? 'Approved' : (report.executive_summary ? 'Analysis Complete' : 'Analysis Pending')} 
        confidence={report.confidence_score}
        generatedAt={report.generated_at}
        reportId={report.id}
        pipelineId={pipelineId}
      />

      <div className="flex flex-col gap-8 w-full mt-4">
        {/* Accordion Sections */}
        <div className="flex flex-col gap-2">
          <EvidenceExplorer report={report} />
          <ReasoningChain report={report} />
          <BiasAnalysis report={report} />
          <ConfidenceAnalysis report={report} />
          <LimitationsPanel />
          <AuditTrail report={report} pipelineStatus={pipelineStatus} />
        </div>

        {/* Raw JSON viewer */}
        <section className="mt-8">
          <h2 className="text-xl font-semibold tracking-tight mb-4">Raw Execution Trace</h2>
          <ExplainabilityJSON data={rawPayload} />
        </section>
      </div>
    </motion.div>
  );
}
