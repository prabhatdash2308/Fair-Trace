import { create } from 'zustand';

/**
 * Dashboard store — placeholder for global dashboard UI state.
 * Data fetching is handled by React Query, not stored here.
 */
interface DashboardState {
  selectedPeriod: string;
  setSelectedPeriod: (period: string) => void;
}

export const useDashboardStore = create<DashboardState>()((set) => ({
  selectedPeriod: '30d',
  setSelectedPeriod: (period) => set({ selectedPeriod: period }),
}));
