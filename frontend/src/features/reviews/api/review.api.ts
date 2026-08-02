import apiClient from '@/api/client';
import { API_ENDPOINTS } from '@/constants/api';
import type {
  ReviewCycle,
  PaginatedCycles,
  ReviewInput,
  CreateCycleRequest,
  UpdateCycleStatusRequest,
  SubmitInputRequest,
  CycleListParams,
} from '../types/review.types';

export const reviewApi = {
  list: (params: CycleListParams = {}) =>
    apiClient
      .get<PaginatedCycles>(API_ENDPOINTS.CYCLES.LIST, { params })
      .then((r) => r.data),

  get: (id: string) =>
    apiClient
      .get<ReviewCycle>(API_ENDPOINTS.CYCLES.GET(id))
      .then((r) => r.data),

  create: (data: CreateCycleRequest) =>
    apiClient
      .post<ReviewCycle>(API_ENDPOINTS.CYCLES.CREATE, data)
      .then((r) => r.data),

  updateStatus: (id: string, data: UpdateCycleStatusRequest) =>
    apiClient
      .patch<ReviewCycle>(API_ENDPOINTS.CYCLES.STATUS(id), data)
      .then((r) => r.data),

  listInputs: (cycleId: string) =>
    apiClient
      .get<ReviewInput[]>(API_ENDPOINTS.CYCLES.INPUTS(cycleId))
      .then((r) => r.data),

  submitInput: (cycleId: string, data: SubmitInputRequest) =>
    apiClient
      .post<ReviewInput>(API_ENDPOINTS.CYCLES.INPUTS(cycleId), data)
      .then((r) => r.data),

  triggerPipeline: (cycleId: string) =>
    apiClient
      .post(API_ENDPOINTS.CYCLES.TRIGGER(cycleId))
      .then((r) => r.data),
};
