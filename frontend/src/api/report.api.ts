import apiClient from './client';
import { API_ENDPOINTS } from '@/constants/api';
import type { Report } from '@/types';

export const reportApi = {
  get: (id: string) =>
    apiClient.get<Report>(API_ENDPOINTS.REPORTS.GET(id)).then((r) => r.data),

  approve: (
    id: string,
    data: { action: string; reason: string; idempotency_key: string }
  ) =>
    apiClient.patch<Report>(API_ENDPOINTS.REPORTS.STATUS(id), data).then((r) => r.data),

  getVersions: (id: string) =>
    apiClient.get<Report[]>(API_ENDPOINTS.REPORTS.VERSIONS(id)).then((r) => r.data),
};
