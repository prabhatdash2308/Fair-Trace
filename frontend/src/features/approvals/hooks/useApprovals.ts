import { useMutation, useQueryClient } from '@tanstack/react-query';
import { v4 as uuidv4 } from 'uuid';
import { reportApi } from '@/features/reports/api/report.api';
import { QUERY_KEYS } from '@/constants/api';
import type { ApprovalAction } from '@/features/reports';
import type { SubmitApprovalForm } from '../types/approval.types';

/**
 * useSubmitApproval — wraps the report approval action with idempotency key generation.
 * The backend requires a UUID v4 idempotency_key (36 chars) on every approval action.
 * This hook generates it automatically so components don't need to.
 */
export function useSubmitApproval(reportId: string) {
  const qc = useQueryClient();

  return useMutation({
    mutationFn: ({ action, reason }: SubmitApprovalForm) =>
      reportApi.approve(reportId, {
        action,
        reason,
        idempotency_key: uuidv4(), // Auto-generated per submission
      }),
    onSuccess: () => {
      void qc.invalidateQueries({ queryKey: QUERY_KEYS.reports.detail(reportId) });
      void qc.invalidateQueries({ queryKey: QUERY_KEYS.reports.versions(reportId) });
      void qc.invalidateQueries({ queryKey: QUERY_KEYS.cycles.all });
    },
  });
}
