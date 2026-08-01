/**
 * API domain types — mirrors backend Pydantic models.
 * Migrated and extended from src/api.ts.
 */

export type UserRole = 'ADMIN' | 'MANAGER' | 'EMPLOYEE';

export type CycleStatus =
  | 'DRAFT'
  | 'ACTIVE'
  | 'PROCESSING'
  | 'PENDING_APPROVAL'
  | 'COMPLETED'
  | 'CANCELLED';

export type ReportStatus =
  | 'DRAFT'
  | 'PENDING_APPROVAL'
  | 'FINALIZED'
  | 'REVISION_REQUESTED'
  | 'REJECTED';

export type ConfidenceLevel = 'HIGH' | 'MEDIUM' | 'LOW' | 'INSUFFICIENT';

export type BiasType =
  | 'RECENCY'
  | 'HALO'
  | 'HORN'
  | 'LENIENCY'
  | 'SEVERITY'
  | 'UNSUPPORTED'
  | 'IMBALANCE';

export type Severity = 'HIGH' | 'MEDIUM' | 'LOW';

export type PipelineRunStatus =
  | 'PENDING'
  | 'RUNNING'
  | 'COMPLETED'
  | 'FAILED'
  | 'HALTED';

// ── Entity types ─────────────────────────────────────────────────────

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: UserRole;
  manager_id?: string;
  is_active: boolean;
  created_at: string;
}

export interface ReviewCycle {
  id: string;
  employee_id: string;
  manager_id: string;
  title: string;
  review_period_start: string;
  review_period_end: string;
  status: CycleStatus;
  created_at: string;
}

export interface ReviewInput {
  id: string;
  review_cycle_id: string;
  input_type: string;
  content_text: string;
  is_anonymized: boolean;
  submitted_at: string;
}

export interface Citation {
  id: string;
  review_input_id: string;
  extracted_passage: string;
  similarity_score: number;
  retrieval_rank: number;
}

export interface Claim {
  id: string;
  dimension: string;
  claim_text: string;
  explanation: string;
  confidence: ConfidenceLevel;
  is_supported: boolean;
  display_order: number;
  citations: Citation[];
}

export interface BiasFlag {
  id: string;
  bias_type: BiasType;
  severity: Severity;
  affected_text?: string;
  recommended_action: string;
  detection_reasoning: string;
  detected_at: string;
}

export interface Report {
  id: string;
  review_cycle_id: string;
  version: number;
  status: ReportStatus;
  executive_summary?: string;
  recommended_actions?: string[];
  confidence_score?: ConfidenceLevel;
  confidence_explanation?: string;
  approved_by?: string;
  approved_at?: string;
  approval_reason?: string;
  claims: Claim[];
  bias_flags: BiasFlag[];
  generated_at: string;
  pipeline_run_id: string;
}

export interface AgentExecution {
  agent_name: string;
  status: string;
  start_time: string;
  end_time?: string;
  output_summary: string;
  error_message?: string;
  latency_ms?: number;
  tokens_total?: number;
  estimated_cost_usd?: number;
  llm_model_used?: string;
  prompt_version?: string;
}

export interface PipelineStatus {
  pipeline_run_id: string;
  review_cycle_id: string;
  pipeline_status: PipelineRunStatus;
  current_agent: string;
  agent_executions: AgentExecution[];
  pipeline_total_tokens?: number;
  pipeline_total_cost_usd?: number;
  created_at: string;
  completed_at?: string;
  error_state?: Record<string, unknown>;
}

export interface AuditEvent {
  id: string;
  event_type: string;
  actor_id?: string;
  actor_role?: UserRole;
  resource_type: string;
  resource_id: string;
  event_payload: Record<string, unknown>;
  occurred_at: string;
  correlation_id?: string;
}

// ── Request/Response wrappers ────────────────────────────────────────

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  skip: number;
  limit: number;
}

export interface ApiError {
  message: string;
  code?: string;
  status: number;
  details?: Record<string, unknown>;
}
