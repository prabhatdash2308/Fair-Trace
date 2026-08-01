import apiClient from './client';
import { API_ENDPOINTS } from '@/constants/api';
import type { AuditEvent } from '@/types';

export const auditApi = {
  list: (params?: { skip?: number; limit?: number }) =>
    apiClient.get<AuditEvent[]>(API_ENDPOINTS.AUDIT.LIST, { params }).then((r) => r.data),

  getForResource: (type: string, id: string) =>
    apiClient.get<AuditEvent[]>(API_ENDPOINTS.AUDIT.RESOURCE(type, id)).then((r) => r.data),

  getForPipeline: (runId: string) =>
    apiClient.get<AuditEvent[]>(API_ENDPOINTS.AUDIT.PIPELINE(runId)).then((r) => r.data),
};
