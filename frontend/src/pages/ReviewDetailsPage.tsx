import * as React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { pageTransition } from '@/components/motion';
import { IconButton } from '@/components/ui/IconButton';
import { ArrowLeft, Loader2 } from 'lucide-react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ROUTES } from '@/constants/routes';

import { useReviewCycle } from '@/features/reviews/hooks/useReviews';
import { useEmployee } from '@/features/employees/hooks/useEmployees';

import {
  ReviewDetailsTop,
  ReviewOverview,
  ReviewScores,
  ReviewPipelineTab,
  ReviewApprovalTab,
  ReviewDocumentsTab,
  ReviewEvidenceTab,
  ReviewTimelineTab
} from '@/features/reviews/components';

export default function ReviewDetailsPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const { data: cycle, isLoading: isCycleLoading } = useReviewCycle(id || '');
  // Fetch employee details using the employee_id from cycle
  const { data: employeeData, isLoading: isEmployeeLoading } = useEmployee(cycle?.employee_id || '');

  if (isCycleLoading) {
    return (
      <div className="flex h-[80vh] items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
      </div>
    );
  }

  if (!cycle) {
    return (
      <div className="flex flex-col items-center justify-center h-[80vh] text-center">
        <h2 className="text-lg font-semibold">Review Not Found</h2>
        <p className="text-muted-foreground mt-2 mb-4">The review cycle you are looking for does not exist.</p>
        <button className="btn btn-secondary" onClick={() => navigate(ROUTES.REVIEWS)}>Back to Reviews</button>
      </div>
    );
  }

  return (
    <motion.div
      variants={pageTransition}
      initial="hidden"
      animate="visible"
      exit="exit"
      className="flex flex-col gap-6 pb-12 w-full max-w-7xl mx-auto"
    >
      <div className="flex items-center gap-2 -mb-2">
        <IconButton icon={ArrowLeft} variant="ghost" onClick={() => navigate(ROUTES.REVIEWS)} />
        <span className="text-sm font-medium text-muted-foreground">Back to Reviews</span>
      </div>

      <ReviewDetailsTop 
        cycle={cycle} 
        employee={employeeData || null} 
        pipelineStatus={cycle.status === 'PROCESSING' ? 'RUNNING' : 'PENDING'} 
      />

      <div className="rounded-xl border border-border/50 bg-card shadow-sm p-6">
        <Tabs defaultValue="overview" className="w-full">
          <div className="border-b border-border/50 px-2 mb-6 overflow-x-auto">
            <TabsList className="bg-transparent h-10 p-0 space-x-6 min-w-max justify-start flex">
              <TabsTrigger value="overview" className="data-[state=active]:bg-transparent data-[state=active]:shadow-none data-[state=active]:border-b-2 data-[state=active]:border-primary rounded-none px-0 h-10">Overview</TabsTrigger>
              <TabsTrigger value="scores" className="data-[state=active]:bg-transparent data-[state=active]:shadow-none data-[state=active]:border-b-2 data-[state=active]:border-primary rounded-none px-0 h-10">AI Scores</TabsTrigger>
              <TabsTrigger value="pipeline" className="data-[state=active]:bg-transparent data-[state=active]:shadow-none data-[state=active]:border-b-2 data-[state=active]:border-primary rounded-none px-0 h-10">Pipeline</TabsTrigger>
              <TabsTrigger value="evidence" className="data-[state=active]:bg-transparent data-[state=active]:shadow-none data-[state=active]:border-b-2 data-[state=active]:border-primary rounded-none px-0 h-10">Evidence</TabsTrigger>
              <TabsTrigger value="documents" className="data-[state=active]:bg-transparent data-[state=active]:shadow-none data-[state=active]:border-b-2 data-[state=active]:border-primary rounded-none px-0 h-10">Documents</TabsTrigger>
              <TabsTrigger value="timeline" className="data-[state=active]:bg-transparent data-[state=active]:shadow-none data-[state=active]:border-b-2 data-[state=active]:border-primary rounded-none px-0 h-10">Timeline</TabsTrigger>
              <TabsTrigger value="approval" className="data-[state=active]:bg-transparent data-[state=active]:shadow-none data-[state=active]:border-b-2 data-[state=active]:border-primary rounded-none px-0 h-10">Approval</TabsTrigger>
            </TabsList>
          </div>

          <TabsContent value="overview" className="mt-0">
            <ReviewOverview cycle={cycle} />
          </TabsContent>
          <TabsContent value="scores" className="mt-0">
            <ReviewScores />
          </TabsContent>
          <TabsContent value="pipeline" className="mt-0">
            <ReviewPipelineTab cycle={cycle} />
          </TabsContent>
          <TabsContent value="evidence" className="mt-0">
            <ReviewEvidenceTab />
          </TabsContent>
          <TabsContent value="documents" className="mt-0">
            <ReviewDocumentsTab />
          </TabsContent>
          <TabsContent value="timeline" className="mt-0">
            <ReviewTimelineTab cycle={cycle} />
          </TabsContent>
          <TabsContent value="approval" className="mt-0">
            <ReviewApprovalTab />
          </TabsContent>
        </Tabs>
      </div>
    </motion.div>
  );
}
