/**
 * Review Cycles feature types.
 * Mirrors: backend/models/schemas.py — ReviewCycleResponse, InputResponse, PaginatedReviewCycles
 *          backend/models/enums.py   — ReviewCycleStatus, InputType
 */

export type ReviewCycleStatus =
  | 'DRAFT'
  | 'ACTIVE'
  | 'PROCESSING'
  | 'PENDING_APPROVAL'
  | 'COMPLETED'
  | 'CANCELLED';

export type InputType =
  | 'SELF_ASSESSMENT'
  | 'MANAGER_NOTE'
  | 'PEER_REVIEW'
  | 'PROJECT_OUTCOME'
  | 'GOAL'
  | 'MEETING_NOTE';

export interface ReviewCycle {
  id: string;
  employee_id: string;
  manager_id: string;
  title: string;
  review_period_start: string; // ISO date (YYYY-MM-DD)
  review_period_end: string;
  status: ReviewCycleStatus;
  created_at: string;
  updated_at: string;
}

export interface PaginatedCycles {
  items: ReviewCycle[];
  total: number;
  skip: number;
  limit: number;
  has_more: boolean;
}

export interface ReviewInput {
  id: string;
  review_cycle_id: string;
  input_type: InputType;
  content_text: string;
  is_anonymized: boolean;
  submitted_at: string;
}

export interface CreateCycleRequest {
  employee_id: string;
  title: string;
  review_period_start: string;
  review_period_end: string;
}

export interface UpdateCycleStatusRequest {
  status: ReviewCycleStatus;
}

export interface SubmitInputRequest {
  input_type: InputType;
  content_text: string;
  is_anonymized?: boolean;
}

export interface CycleListParams {
  skip?: number;
  limit?: number;
}
