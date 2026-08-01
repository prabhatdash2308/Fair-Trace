import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { QUERY_KEYS } from '@/constants/api';
import { reviewApi } from '../api/review.api';
import type {
  CreateCycleRequest,
  UpdateCycleStatusRequest,
  SubmitInputRequest,
  CycleListParams,
} from '../types/review.types';

export function useReviewCycles(params: CycleListParams = {}) {
  return useQuery({
    queryKey: QUERY_KEYS.cycles.list(params),
    queryFn:  () => reviewApi.list(params),
    staleTime: 60 * 1000, // 1 minute
  });
}

export function useReviewCycle(id: string) {
  return useQuery({
    queryKey: QUERY_KEYS.cycles.detail(id),
    queryFn:  () => reviewApi.get(id),
    enabled:  !!id,
  });
}

export function useCycleInputs(cycleId: string) {
  return useQuery({
    queryKey: QUERY_KEYS.cycles.inputs(cycleId),
    queryFn:  () => reviewApi.listInputs(cycleId),
    enabled:  !!cycleId,
  });
}

export function useCreateCycle() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: CreateCycleRequest) => reviewApi.create(data),
    onSuccess: () => {
      void qc.invalidateQueries({ queryKey: QUERY_KEYS.cycles.all });
    },
  });
}

export function useUpdateCycleStatus(cycleId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: UpdateCycleStatusRequest) =>
      reviewApi.updateStatus(cycleId, data),
    onSuccess: () => {
      void qc.invalidateQueries({ queryKey: QUERY_KEYS.cycles.detail(cycleId) });
      void qc.invalidateQueries({ queryKey: QUERY_KEYS.cycles.all });
    },
  });
}

export function useSubmitInput(cycleId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: SubmitInputRequest) =>
      reviewApi.submitInput(cycleId, data),
    onSuccess: () => {
      void qc.invalidateQueries({ queryKey: QUERY_KEYS.cycles.inputs(cycleId) });
    },
  });
}
