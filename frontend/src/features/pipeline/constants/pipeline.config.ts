export interface PipelineStepConfig {
  id: string;
  title: string;
  order: number;
}

export const PIPELINE_STEPS: PipelineStepConfig[] = [
  { id: 'intake', title: 'Intake', order: 1 },
  { id: 'embedding', title: 'Embedding', order: 2 },
  { id: 'evidence_retrieval', title: 'Evidence Retrieval', order: 3 },
  { id: 'bias_detection', title: 'Bias Detection', order: 4 },
  { id: 'performance_analysis', title: 'Performance Analysis', order: 5 },
  { id: 'explainability', title: 'Explainability', order: 6 },
  { id: 'report_generation', title: 'Report Generation', order: 7 },
  { id: 'human_approval', title: 'Human Approval', order: 8 },
  { id: 'finalization', title: 'Finalization', order: 9 },
];
