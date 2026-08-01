import apiClient from '@/api/client';
import { API_ENDPOINTS } from '@/constants/api';
import type { AuditEvent, AuditListParams } from '../types/audit.types';

export const auditApi = {
  list: (params: AuditListParams = {}) =>
    apiClient
      .get<AuditEvent[]>(API_ENDPOINTS.AUDIT.LIST, { params })
      .then((r) => r.data),

  getForResource: (resourceType: string, resourceId: string, params?: AuditListParams) =>
    apiClient
      .get<AuditEvent[]>(API_ENDPOINTS.AUDIT.RESOURCE(resourceType, resourceId), { params })
      .then((r) => r.data),

  getForPipeline: (runId: string) =>
    apiClient
      .get<AuditEvent[]>(API_ENDPOINTS.AUDIT.PIPELINE(runId))
      .then((r) => r.data),
};
