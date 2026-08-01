import * as React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { pageTransition } from '@/components/motion';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { IconButton } from '@/components/ui/IconButton';
import { ArrowLeft } from 'lucide-react';
import { useEmployee } from '@/features/employees/hooks/useEmployees';

import {
  EmployeeProfile,
  EmployeeOverview,
  EmployeePerformance,
  EmployeeReviews,
  EmployeeDocuments,
  EmployeeInsights,
  EmployeeTimeline,
} from '@/features/employees/components';

export default function EmployeeDetailsPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: employee, isLoading, error } = useEmployee(id || '');

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="spinner-lg" />
      </div>
    );
  }

  if (error || !employee) {
    return (
      <div className="flex flex-col items-center justify-center h-64 text-center">
        <h2 className="text-lg font-semibold">Employee Not Found</h2>
        <p className="text-muted-foreground mt-2 mb-4">The employee you are looking for does not exist or you do not have permission to view them.</p>
        <button className="btn btn-secondary" onClick={() => navigate('/employees')}>Back to Employees</button>
      </div>
    );
  }

  return (
    <motion.div
      variants={pageTransition}
      initial="hidden"
      animate="visible"
      exit="exit"
      className="flex flex-col gap-8 pb-12 max-w-6xl mx-auto w-full"
    >
      {/* Top Back Navigation */}
      <div className="flex items-center gap-2 -mb-2">
        <IconButton icon={ArrowLeft} variant="ghost" onClick={() => navigate('/employees')} />
        <span className="text-sm font-medium text-muted-foreground">Back to Directory</span>
      </div>

      {/* Hero Profile */}
      <EmployeeProfile employee={employee} />

      {/* Tab Navigation */}
      <Tabs defaultValue="overview" className="w-full">
        <div className="border-b border-border/50 px-2">
          <TabsList className="bg-transparent h-12 p-0 space-x-6">
            <TabsTrigger value="overview" className="data-[state=active]:bg-transparent data-[state=active]:shadow-none data-[state=active]:border-b-2 data-[state=active]:border-primary rounded-none px-0 h-12">Overview</TabsTrigger>
            <TabsTrigger value="performance" className="data-[state=active]:bg-transparent data-[state=active]:shadow-none data-[state=active]:border-b-2 data-[state=active]:border-primary rounded-none px-0 h-12">Performance</TabsTrigger>
            <TabsTrigger value="reviews" className="data-[state=active]:bg-transparent data-[state=active]:shadow-none data-[state=active]:border-b-2 data-[state=active]:border-primary rounded-none px-0 h-12">Reviews</TabsTrigger>
            <TabsTrigger value="documents" className="data-[state=active]:bg-transparent data-[state=active]:shadow-none data-[state=active]:border-b-2 data-[state=active]:border-primary rounded-none px-0 h-12">Documents</TabsTrigger>
            <TabsTrigger value="insights" className="data-[state=active]:bg-transparent data-[state=active]:shadow-none data-[state=active]:border-b-2 data-[state=active]:border-primary rounded-none px-0 h-12">AI Insights</TabsTrigger>
            <TabsTrigger value="timeline" className="data-[state=active]:bg-transparent data-[state=active]:shadow-none data-[state=active]:border-b-2 data-[state=active]:border-primary rounded-none px-0 h-12">Timeline</TabsTrigger>
          </TabsList>
        </div>

        <div className="mt-8">
          <TabsContent value="overview"><EmployeeOverview employee={employee} /></TabsContent>
          <TabsContent value="performance"><EmployeePerformance /></TabsContent>
          <TabsContent value="reviews"><EmployeeReviews /></TabsContent>
          <TabsContent value="documents"><EmployeeDocuments /></TabsContent>
          <TabsContent value="insights"><EmployeeInsights /></TabsContent>
          <TabsContent value="timeline"><EmployeeTimeline employee={employee} /></TabsContent>
        </div>
      </Tabs>
    </motion.div>
  );
}
