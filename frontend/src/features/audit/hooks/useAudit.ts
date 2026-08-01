import { useQuery } from '@tanstack/react-query';
import { QUERY_KEYS } from '@/constants/api';
import { auditApi } from '../api/audit.api';
import type { AuditListParams } from '../types/audit.types';

export function useAuditEvents(params: AuditListParams = {}) {
  return useQuery({
    queryKey: QUERY_KEYS.audit.list(params),
    queryFn:  () => auditApi.list(params),
    staleTime: 30 * 1000, // 30 seconds
  });
}

export function useResourceAuditEvents(resourceType: string, resourceId: string) {
  return useQuery({
    queryKey: QUERY_KEYS.audit.resource(resourceType, resourceId),
    queryFn:  () => auditApi.getForResource(resourceType, resourceId),
    enabled:  !!resourceType && !!resourceId,
    staleTime: 30 * 1000,
  });
}

export function usePipelineAuditEvents(runId: string | null) {
  return useQuery({
    queryKey: QUERY_KEYS.audit.pipeline(runId ?? ''),
    queryFn:  () => auditApi.getForPipeline(runId!),
    enabled:  !!runId,
    staleTime: 10 * 1000, // 10 seconds — pipeline events change frequently
  });
}
