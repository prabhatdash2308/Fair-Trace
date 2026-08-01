// ReviewGuard AI — Axios API Client + TypeScript Types

import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
})

// ── Auth Token Injection ──────────────────────────────────────────
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('rg_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// ── Error Handling ────────────────────────────────────────────────
api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('rg_token')
      localStorage.removeItem('rg_user')
      window.location.href = '/login'
    }
    return Promise.reject(err)
  }
)

// ── Types ──────────────────────────────────────────────────────────
export type UserRole = 'ADMIN' | 'MANAGER' | 'EMPLOYEE'
export type CycleStatus = 'DRAFT' | 'ACTIVE' | 'PROCESSING' | 'PENDING_APPROVAL' | 'COMPLETED' | 'CANCELLED'
export type ReportStatus = 'DRAFT' | 'PENDING_APPROVAL' | 'FINALIZED' | 'REVISION_REQUESTED' | 'REJECTED'
export type ConfidenceLevel = 'HIGH' | 'MEDIUM' | 'LOW' | 'INSUFFICIENT'
export type BiasType = 'RECENCY' | 'HALO' | 'HORN' | 'LENIENCY' | 'SEVERITY' | 'UNSUPPORTED' | 'IMBALANCE'
export type Severity = 'HIGH' | 'MEDIUM' | 'LOW'

export interface User { id: string; email: string; full_name: string; role: UserRole; manager_id?: string; is_active: boolean; created_at: string }
export interface ReviewCycle { id: string; employee_id: string; manager_id: string; title: string; review_period_start: string; review_period_end: string; status: CycleStatus; created_at: string }
export interface ReviewInput { id: string; review_cycle_id: string; input_type: string; content_text: string; is_anonymized: boolean; submitted_at: string }
export interface Citation { id: string; review_input_id: string; extracted_passage: string; similarity_score: number; retrieval_rank: number }
export interface Claim { id: string; dimension: string; claim_text: string; explanation: string; confidence: ConfidenceLevel; is_supported: boolean; display_order: number; citations: Citation[] }
export interface BiasFlag { id: string; bias_type: BiasType; severity: Severity; affected_text?: string; recommended_action: string; detection_reasoning: string; detected_at: string }
export interface Report { id: string; review_cycle_id: string; version: number; status: ReportStatus; executive_summary?: string; recommended_actions?: string[]; confidence_score?: ConfidenceLevel; confidence_explanation?: string; approved_by?: string; approved_at?: string; approval_reason?: string; claims: Claim[]; bias_flags: BiasFlag[]; generated_at: string; pipeline_run_id: string }
export interface AgentExecution { agent_name: string; status: string; start_time: string; end_time?: string; output_summary: string; error_message?: string; latency_ms?: number; tokens_total?: number; estimated_cost_usd?: number; llm_model_used?: string; prompt_version?: string }
export interface PipelineStatus { pipeline_run_id: string; review_cycle_id: string; pipeline_status: string; current_agent: string; agent_executions: AgentExecution[]; pipeline_total_tokens?: number; pipeline_total_cost_usd?: number; created_at: string; completed_at?: string; error_state?: Record<string, unknown> }
export interface AuditEvent { id: string; event_type: string; actor_id?: string; actor_role?: UserRole; resource_type: string; resource_id: string; event_payload: Record<string, unknown>; occurred_at: string; correlation_id?: string }

// ── API Functions ──────────────────────────────────────────────────
export const authApi = {
  login: (email: string, password: string) =>
    api.post('/auth/login', { email, password }).then(r => r.data),
}

export const usersApi = {
  list: (skip = 0, limit = 20) => api.get('/users', { params: { skip, limit } }).then(r => r.data),
  create: (data: { email: string; password: string; full_name: string; role: UserRole; manager_id?: string }) =>
    api.post('/users', data).then(r => r.data),
  getMe: (id: string) => api.get(`/users/${id}`).then(r => r.data),
}

export const cyclesApi = {
  list: (skip = 0, limit = 20) => api.get('/review-cycles', { params: { skip, limit } }).then(r => r.data),
  get: (id: string) => api.get(`/review-cycles/${id}`).then(r => r.data),
  create: (data: { employee_id: string; title: string; review_period_start: string; review_period_end: string }) =>
    api.post('/review-cycles', data).then(r => r.data),
  updateStatus: (id: string, status: CycleStatus) =>
    api.patch(`/review-cycles/${id}/status`, { status }).then(r => r.data),
  getInputs: (id: string) => api.get(`/review-cycles/${id}/inputs`).then(r => r.data),
  submitInput: (id: string, data: { input_type: string; content_text: string; is_anonymized: boolean }) =>
    api.post(`/review-cycles/${id}/inputs`, data).then(r => r.data),
  triggerPipeline: (id: string) =>
    api.post(`/review-cycles/${id}/pipeline/trigger`).then(r => r.data),
}

export const pipelineApi = {
  getStatus: (runId: string) => api.get(`/pipeline/${runId}/status`).then(r => r.data),
}

export const reportsApi = {
  get: (id: string) => api.get(`/reports/${id}`).then(r => r.data),
  approve: (id: string, data: { action: string; reason: string; idempotency_key: string }) =>
    api.patch(`/reports/${id}/status`, data).then(r => r.data),
  getVersions: (id: string) => api.get(`/reports/${id}/versions`).then(r => r.data),
}

export const auditApi = {
  list: (skip = 0, limit = 50) => api.get('/audit', { params: { skip, limit } }).then(r => r.data),
  getForResource: (type: string, id: string) => api.get(`/audit/resource/${type}/${id}`).then(r => r.data),
  getForPipeline: (runId: string) => api.get(`/audit/pipeline/${runId}`).then(r => r.data),
}

export default api
