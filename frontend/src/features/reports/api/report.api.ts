import apiClient from '@/api/client';
import { API_ENDPOINTS } from '@/constants/api';
import type { Report, ReportVersionSummary, ApprovalActionRequest } from '../types/report.types';

export const reportApi = {
  get: (id: string) =>
    apiClient
      .get<Report>(API_ENDPOINTS.REPORTS.GET(id))
      .then((r) => r.data),

  approve: (id: string, data: ApprovalActionRequest) =>
    apiClient
      .patch<Report>(API_ENDPOINTS.REPORTS.STATUS(id), data)
      .then((r) => r.data),

  getVersions: (id: string) =>
    apiClient
      .get<ReportVersionSummary[]>(API_ENDPOINTS.REPORTS.VERSIONS(id))
      .then((r) => r.data),
};
