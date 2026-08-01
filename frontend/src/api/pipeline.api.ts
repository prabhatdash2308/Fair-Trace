import apiClient from './client';
import { API_ENDPOINTS } from '@/constants/api';
import type { PipelineStatus } from '@/types';

export const pipelineApi = {
  getStatus: (runId: string) =>
    apiClient.get<PipelineStatus>(API_ENDPOINTS.PIPELINE.STATUS(runId)).then((r) => r.data),
};
