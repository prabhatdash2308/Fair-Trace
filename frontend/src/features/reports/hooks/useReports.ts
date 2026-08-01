import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { QUERY_KEYS } from '@/constants/api';
import { reportApi } from '../api/report.api';
import type { ApprovalActionRequest } from '../types/report.types';

export function useReport(id: string) {
  return useQuery({
    queryKey: QUERY_KEYS.reports.detail(id),
    queryFn:  () => reportApi.get(id),
    enabled:  !!id,
    staleTime: 2 * 60 * 1000,
  });
}

export function useReportVersions(id: string) {
  return useQuery({
    queryKey: QUERY_KEYS.reports.versions(id),
    queryFn:  () => reportApi.getVersions(id),
    enabled:  !!id,
  });
}

/**
 * useApprovalAction — APPROVE / REVISION_REQUESTED / REJECT a report.
 * Invalidates both the report detail and versions on success.
 */
export function useApprovalAction(reportId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: ApprovalActionRequest) =>
      reportApi.approve(reportId, data),
    onSuccess: () => {
      void qc.invalidateQueries({ queryKey: QUERY_KEYS.reports.detail(reportId) });
      void qc.invalidateQueries({ queryKey: QUERY_KEYS.reports.versions(reportId) });
      // Invalidate cycles list too — status may have changed to COMPLETED
      void qc.invalidateQueries({ queryKey: QUERY_KEYS.cycles.all });
    },
  });
}
