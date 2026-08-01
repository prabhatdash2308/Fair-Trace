import type { PipelineStatusResponse, AgentExecution } from '../types/pipeline.types';
import { PIPELINE_STEPS } from '../constants/pipeline.config';
import { normalizeAgentStatus, normalizePipelineStatus, PIPELINE_STATUS_MAP, type StatusConfig, type NormalizedStatus } from '../constants/pipelineStatus';

export interface UINode {
  id: string;
  title: string;
  order: number;
  statusConfig: StatusConfig;
  statusLabel: string;
  normalizedStatus: NormalizedStatus;
  startTime: string | null;
  endTime: string | null;
  latencyMs: number | null;
  tokensTotal: number | null;
  costUsd: number | null;
  logs: string;
  error: string | null;
}

export interface UIPipeline {
  runId: string;
  statusConfig: StatusConfig;
  statusLabel: string;
  progress: number;
  currentNode: string;
  nodes: UINode[];
  totalTokens: number;
  totalCostUsd: number;
  totalLatencyMs: number;
  startedAt: string;
  completedAt: string | null;
}

export const normalizePipeline = (data: PipelineStatusResponse | null): UIPipeline | null => {
  if (!data) return null;

  const normalizedPipelineStatus = normalizePipelineStatus(data.pipeline_status);
  const pipelineStatusConfig = PIPELINE_STATUS_MAP[normalizedPipelineStatus];

  let totalLatency = 0;
  let totalTokens = data.pipeline_total_tokens || 0;
  let totalCostUsd = data.pipeline_total_cost_usd || 0;
  
  let completedCount = 0;

  const nodes: UINode[] = PIPELINE_STEPS.map((step) => {
    // Find matching agent execution by matching step ID to agent_name loosely 
    // (assuming backend sends agent_name similar to step.id)
    const exec = data.agent_executions.find((a) => a.agent_name.toLowerCase() === step.id.toLowerCase());

    let normalizedStatus: NormalizedStatus = 'PENDING';
    if (exec) {
      normalizedStatus = normalizeAgentStatus(exec.status);
    } else if (normalizedPipelineStatus === 'COMPLETED') {
      normalizedStatus = 'SKIPPED'; // If pipeline is done but node wasn't executed
    }

    if (normalizedStatus === 'COMPLETED') completedCount++;

    const statusConfig = PIPELINE_STATUS_MAP[normalizedStatus];

    if (exec?.latency_ms) totalLatency += exec.latency_ms;

    return {
      id: step.id,
      title: step.title,
      order: step.order,
      statusConfig,
      statusLabel: statusConfig.label,
      normalizedStatus,
      startTime: exec?.start_time || null,
      endTime: exec?.end_time || null,
      latencyMs: exec?.latency_ms || null,
      tokensTotal: exec?.tokens_total || null,
      costUsd: exec?.estimated_cost_usd || null,
      logs: exec?.output_summary || '',
      error: exec?.error_message || null,
    };
  });

  const progress = Math.round((completedCount / PIPELINE_STEPS.length) * 100);

  return {
    runId: data.pipeline_run_id,
    statusConfig: pipelineStatusConfig,
    statusLabel: pipelineStatusConfig.label,
    progress: normalizedPipelineStatus === 'COMPLETED' ? 100 : progress,
    currentNode: data.current_agent || 'Starting...',
    nodes,
    totalTokens,
    totalCostUsd,
    totalLatencyMs: totalLatency,
    startedAt: data.created_at,
    completedAt: data.completed_at,
  };
};
