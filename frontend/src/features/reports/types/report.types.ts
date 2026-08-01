/**
 * Reports feature types.
 * Mirrors: backend/models/schemas.py — ReportResponse, ClaimResponse, CitationResponse,
 *          BiasFlagResponse, ReportVersionSummary, ApprovalActionRequest
 *          backend/models/enums.py   — ReportStatus, ConfidenceLevel, PerformanceDimension,
 *          BiasType, Severity, ApprovalAction
 */

export type ReportStatus =
  | 'DRAFT'
  | 'PENDING_APPROVAL'
  | 'FINALIZED'
  | 'REVISION_REQUESTED'
  | 'REJECTED';

export type ConfidenceLevel = 'HIGH' | 'MEDIUM' | 'LOW' | 'INSUFFICIENT';

export type PerformanceDimension =
  | 'TECHNICAL'
  | 'COLLABORATION'
  | 'LEADERSHIP'
  | 'DELIVERY'
  | 'GROWTH';

export type BiasType =
  | 'RECENCY'
  | 'HALO'
  | 'HORN'
  | 'LENIENCY'
  | 'SEVERITY'
  | 'UNSUPPORTED'
  | 'IMBALANCE';

export type Severity = 'HIGH' | 'MEDIUM' | 'LOW';

export type ApprovalAction = 'APPROVE' | 'REVISION_REQUESTED' | 'REJECT';

export interface Citation {
  id: string;
  review_input_id: string;
  extracted_passage: string;
  similarity_score: number;
  retrieval_rank: number;
}

export interface Claim {
  id: string;
  dimension: PerformanceDimension;
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
  affected_text: string | null;
  recommended_action: string;
  detection_reasoning: string;
  detected_at: string;
}

export interface Report {
  id: string;
  review_cycle_id: string;
  version: number;
  status: ReportStatus;
  executive_summary: string | null;
  recommended_actions: string[] | null;
  confidence_score: ConfidenceLevel | null;
  confidence_explanation: string | null;
  approved_by: string | null;
  approved_at: string | null;
  approval_reason: string | null;
  claims: Claim[];
  bias_flags: BiasFlag[];
  generated_at: string;
  pipeline_run_id: string;
}

export interface ReportVersionSummary {
  id: string;
  version: number;
  status: ReportStatus;
  confidence_score: ConfidenceLevel | null;
  generated_at: string;
  is_current: boolean;
}

export interface ApprovalActionRequest {
  action: ApprovalAction;
  reason: string;
  idempotency_key: string; // UUID v4 string — 36 chars
}
