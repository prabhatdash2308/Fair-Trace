/**
 * Approvals feature types.
 * The Human Approval workflow acts on Reports — these types extend report types
 * with approval-specific UI state.
 */

import type { Report, ApprovalAction } from '@/features/reports';

export type ApprovalStatus = 'PENDING' | 'APPROVED' | 'REVISION_REQUESTED' | 'REJECTED';

export interface ApprovalQueueItem {
  report: Report;
  cycle_title: string;
  employee_name: string;
  days_pending: number;
}

export interface SubmitApprovalForm {
  action: ApprovalAction;
  reason: string;
}
