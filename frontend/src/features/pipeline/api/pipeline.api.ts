import apiClient from '@/api/client';
import { API_ENDPOINTS } from '@/constants/api';
import type { PipelineTriggerResponse, PipelineStatusResponse } from '../types/pipeline.types';

export const pipelineApi = {
  trigger: (cycleId: string) =>
    apiClient
      .post<PipelineTriggerResponse>(API_ENDPOINTS.CYCLES.TRIGGER(cycleId))
      .then((r) => r.data),

  getStatus: (runId: string) =>
    apiClient
      .get<PipelineStatusResponse>(API_ENDPOINTS.PIPELINE.STATUS(runId))
      .then((r) => r.data),
};
