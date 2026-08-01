import apiClient from './client';
import { API_ENDPOINTS } from '@/constants/api';
import type { ReviewCycle, ReviewInput, CycleStatus } from '@/types';

export const reviewApi = {
  list: (params?: { skip?: number; limit?: number }) =>
    apiClient.get<ReviewCycle[]>(API_ENDPOINTS.CYCLES.LIST, { params }).then((r) => r.data),

  get: (id: string) =>
    apiClient.get<ReviewCycle>(API_ENDPOINTS.CYCLES.GET(id)).then((r) => r.data),

  create: (data: {
    employee_id: string;
    title: string;
    review_period_start: string;
    review_period_end: string;
  }) => apiClient.post<ReviewCycle>(API_ENDPOINTS.CYCLES.CREATE, data).then((r) => r.data),

  updateStatus: (id: string, status: CycleStatus) =>
    apiClient.patch<ReviewCycle>(API_ENDPOINTS.CYCLES.STATUS(id), { status }).then((r) => r.data),

  getInputs: (id: string) =>
    apiClient.get<ReviewInput[]>(API_ENDPOINTS.CYCLES.INPUTS(id)).then((r) => r.data),

  submitInput: (
    id: string,
    data: { input_type: string; content_text: string; is_anonymized: boolean }
  ) =>
    apiClient.post<ReviewInput>(API_ENDPOINTS.CYCLES.INPUTS(id), data).then((r) => r.data),

  triggerPipeline: (id: string) =>
    apiClient.post(API_ENDPOINTS.CYCLES.TRIGGER(id)).then((r) => r.data),
};
