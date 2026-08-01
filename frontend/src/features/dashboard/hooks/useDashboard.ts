import { useQuery } from '@tanstack/react-query';
import { QUERY_KEYS } from '@/constants/api';
import { reviewApi } from '@/features/reviews/api/review.api';
import type { DashboardKPI } from '../types/dashboard.types';

/**
 * useDashboardKPIs — derives KPI summary from the review cycles list.
 * No dedicated backend endpoint. Uses cycles data already cached by useReviewCycles.
 */
export function useDashboardKPIs() {
  return useQuery({
    queryKey: QUERY_KEYS.dashboard.summary,
    queryFn: async (): Promise<DashboardKPI> => {
      // Fetch a broad window to compute KPIs accurately
      const data = await reviewApi.list({ skip: 0, limit: 100 });

      const now = new Date();
      const thisMonthStart = new Date(now.getFullYear(), now.getMonth(), 1);

      const completedThisMonth = data.items.filter((c) => {
        const updated = new Date(c.updated_at);
        return c.status === 'COMPLETED' && updated >= thisMonthStart;
      }).length;

      return {
        totalCycles:       data.total,
        activeCycles:      data.items.filter((c) => c.status === 'ACTIVE').length,
        pendingApprovals:  data.items.filter((c) => c.status === 'PENDING_APPROVAL').length,
        completedThisMonth,
      };
    },
    staleTime: 60 * 1000, // 1 minute
  });
}

/**
 * useRecentActivity — returns the 5 most recently updated cycles for the activity feed.
 */
export function useRecentActivity(limit = 5) {
  return useQuery({
    queryKey: [...QUERY_KEYS.cycles.list({ limit }), 'recent'],
    queryFn: () => reviewApi.list({ skip: 0, limit }),
    staleTime: 60 * 1000,
    select: (data) => data.items,
  });
}
