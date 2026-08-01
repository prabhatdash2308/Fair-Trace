import { create } from 'zustand';

/**
 * Pipeline store — tracks active pipeline run IDs and polling state.
 */
interface PipelineState {
  activeRunId: string | null;
  isPolling: boolean;

  // Actions
  setActiveRunId: (runId: string | null) => void;
  setPolling: (polling: boolean) => void;
  clearActiveRun: () => void;
}

export const usePipelineStore = create<PipelineState>()((set) => ({
  activeRunId: null,
  isPolling: false,

  setActiveRunId: (activeRunId) => set({ activeRunId }),
  setPolling: (isPolling) => set({ isPolling }),
  clearActiveRun: () => set({ activeRunId: null, isPolling: false }),
}));
