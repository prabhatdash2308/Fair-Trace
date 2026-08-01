/**
 * Pipeline feature types.
 * Mirrors: backend/models/schemas.py — PipelineTriggerResponse, PipelineStatusResponse, AgentExecutionResponse
 */

export type PipelineStatus =
  | 'QUEUED'
  | 'RUNNING'
  | 'COMPLETED'
  | 'FAILED'
  | 'HALTED';

export type AgentStatus = 'PENDING' | 'RUNNING' | 'COMPLETED' | 'FAILED' | 'SKIPPED';

export interface AgentExecution {
  agent_name: string;
  status: AgentStatus;
  start_time: string;
  end_time: string | null;
  output_summary: string;
  error_message: string | null;
  latency_ms: number | null;
  tokens_total: number | null;
  estimated_cost_usd: number | null;
  llm_model_used: string | null;
  prompt_version: string | null;
}

export interface PipelineTriggerResponse {
  pipeline_run_id: string;
  status: string;
  message: string;
}

export interface PipelineStatusResponse {
  pipeline_run_id: string;
  review_cycle_id: string;
  pipeline_status: PipelineStatus;
  current_agent: string;
  agent_executions: AgentExecution[];
  pipeline_total_tokens: number | null;
  pipeline_total_cost_usd: number | null;
  created_at: string;
  completed_at: string | null;
  error_state: Record<string, unknown> | null;
}
