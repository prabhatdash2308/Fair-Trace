import * as React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { pageTransition } from '@/components/motion';
import { IconButton } from '@/components/ui/IconButton';
import { ArrowLeft } from 'lucide-react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

import { usePipelineStatus } from '@/features/pipeline/hooks/usePipeline';
import { normalizePipeline, type UINode } from '@/features/pipeline/utils';

import {
  PipelineHeader,
  PipelineOverview,
  PipelineGraph,
  PipelineTimeline,
  PipelineDiagnostics,
  PipelineLogs,
  PipelineEvidence,
  PipelineLoading
} from '@/features/pipeline/components';

export default function PipelineRunPage() {
  const { runId } = useParams<{ runId: string }>();
  const navigate = useNavigate();
  
  const { data: rawData, isLoading, error } = usePipelineStatus(runId || '');
  
  const pipeline = React.useMemo(() => normalizePipeline(rawData || null), [rawData]);
  const [selectedNodeId, setSelectedNodeId] = React.useState<string>('intake');

  const selectedNode = React.useMemo(() => {
    return pipeline?.nodes.find((n) => n.id === selectedNodeId) || pipeline?.nodes[0];
  }, [pipeline, selectedNodeId]);

  if (isLoading || (!pipeline && !error)) {
    return <PipelineLoading />;
  }

  if (error || !pipeline) {
    return (
      <div className="flex flex-col items-center justify-center h-[80vh] text-center">
        <h2 className="text-lg font-semibold">Pipeline Execution Not Found</h2>
        <p className="text-muted-foreground mt-2 mb-4">The pipeline execution you are looking for does not exist.</p>
        <button className="btn btn-secondary" onClick={() => navigate('/pipeline')}>Back to Pipelines</button>
      </div>
    );
  }

  return (
    <motion.div
      variants={pageTransition}
      initial="hidden"
      animate="visible"
      exit="exit"
      className="flex flex-col gap-8 pb-12 w-full max-w-7xl mx-auto"
    >
      <div className="flex items-center gap-2 -mb-4">
        <IconButton icon={ArrowLeft} variant="ghost" onClick={() => navigate('/pipeline')} />
        <span className="text-sm font-medium text-muted-foreground">Back to Pipeline Monitor</span>
      </div>

      <PipelineHeader pipeline={pipeline} />
      <PipelineOverview pipeline={pipeline} />

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Column: Visual Flow (LangGraph) */}
        <div className="lg:col-span-4 space-y-8">
          <PipelineGraph 
            pipeline={pipeline} 
            selectedNodeId={selectedNodeId} 
            onNodeSelect={(node) => setSelectedNodeId(node.id)} 
          />
          <PipelineTimeline pipeline={pipeline} />
        </div>

        {/* Right Column: Deep Dive Node Tabs */}
        <div className="lg:col-span-8 space-y-6">
          <div className="rounded-lg border border-border/50 bg-card p-6 shadow-sm">
            <h3 className="text-lg font-bold tracking-tight mb-6">
              {selectedNode?.title || 'Node Details'}
            </h3>
            
            <Tabs defaultValue="diagnostics" className="w-full">
              <div className="border-b border-border/50 px-2 mb-6">
                <TabsList className="bg-transparent h-10 p-0 space-x-6">
                  <TabsTrigger value="diagnostics" className="data-[state=active]:bg-transparent data-[state=active]:shadow-none data-[state=active]:border-b-2 data-[state=active]:border-primary rounded-none px-0 h-10">Diagnostics</TabsTrigger>
                  <TabsTrigger value="logs" className="data-[state=active]:bg-transparent data-[state=active]:shadow-none data-[state=active]:border-b-2 data-[state=active]:border-primary rounded-none px-0 h-10">Logs</TabsTrigger>
                  <TabsTrigger value="evidence" className="data-[state=active]:bg-transparent data-[state=active]:shadow-none data-[state=active]:border-b-2 data-[state=active]:border-primary rounded-none px-0 h-10">Evidence</TabsTrigger>
                </TabsList>
              </div>

              {selectedNode && (
                <>
                  <TabsContent value="diagnostics" className="mt-0">
                    <PipelineDiagnostics node={selectedNode} />
                  </TabsContent>
                  <TabsContent value="logs" className="mt-0">
                    <PipelineLogs node={selectedNode} />
                  </TabsContent>
                  <TabsContent value="evidence" className="mt-0">
                    <PipelineEvidence node={selectedNode} />
                  </TabsContent>
                </>
              )}
            </Tabs>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
