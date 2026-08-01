/**
 * Audit feature types.
 * Mirrors: backend/models/schemas.py — AuditEventResponse
 *          backend/models/enums.py   — AuditEventType, UserRole
 */

import type { UserRole } from '@/features/employees';

export type AuditEventType =
  | 'REVIEW_CYCLE_CREATED'
  | 'REVIEW_CYCLE_UPDATED'
  | 'REVIEW_CYCLE_CANCELLED'
  | 'INPUT_SUBMITTED'
  | 'PIPELINE_TRIGGERED'
  | 'PIPELINE_COMPLETED'
  | 'PIPELINE_FAILED'
  | 'AGENT_EXECUTED'
  | 'REPORT_GENERATED'
  | 'REPORT_APPROVED'
  | 'REPORT_REJECTED'
  | 'REPORT_REVISION_REQUESTED'
  | 'USER_LOGIN'
  | 'USER_LOGOUT'
  | 'ACCESS_DENIED';

export interface AuditEvent {
  id: string;
  event_type: AuditEventType;
  actor_id: string | null;
  actor_role: UserRole | null;
  resource_type: string;
  resource_id: string;
  event_payload: Record<string, unknown>;
  occurred_at: string;
  correlation_id: string | null;
  state_version: number | null;
  prompt_version: string | null;
}

export interface AuditListParams {
  skip?: number;
  limit?: number;
}
