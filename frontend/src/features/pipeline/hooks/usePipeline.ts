import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { QUERY_KEYS } from '@/constants/api';
import { usePipelineStore } from '@/store/pipeline/pipeline.store';
import { pipelineApi } from '../api/pipeline.api';
import type { PipelineStatus } from '../types/pipeline.types';

const TERMINAL_STATES: PipelineStatus[] = ['COMPLETED', 'FAILED', 'HALTED'];

/**
 * usePipelineStatus — polls pipeline status until a terminal state is reached.
 * Polling interval: 3 seconds while QUEUED or RUNNING.
 * Stops automatically when pipeline completes, fails, or halts.
 */
export function usePipelineStatus(runId: string | null) {
  return useQuery({
    queryKey: QUERY_KEYS.pipeline.status(runId ?? ''),
    queryFn:  () => pipelineApi.getStatus(runId!),
    enabled:  !!runId,
    refetchInterval: (query) => {
      const status = query.state.data?.pipeline_status;
      if (!status || TERMINAL_STATES.includes(status as PipelineStatus)) {
        return false; // Stop polling
      }
      return 3000; // Poll every 3 seconds
    },
    staleTime: 0, // Always re-fetch when polling
  });
}

/**
 * useTriggerPipeline — fires the pipeline and stores the run ID in Zustand
 * so any component can subscribe to polling status.
 */
export function useTriggerPipeline() {
  const qc = useQueryClient();
  const { setActiveRunId, setPolling } = usePipelineStore();

  return useMutation({
    mutationFn: (cycleId: string) => pipelineApi.trigger(cycleId),
    onSuccess: (data) => {
      setActiveRunId(data.pipeline_run_id);
      setPolling(true);
      // Prime the cache with an initial status query
      void qc.prefetchQuery({
        queryKey: QUERY_KEYS.pipeline.status(data.pipeline_run_id),
        queryFn: () => pipelineApi.getStatus(data.pipeline_run_id),
      });
    },
    onError: () => {
      setPolling(false);
    },
  });
}
