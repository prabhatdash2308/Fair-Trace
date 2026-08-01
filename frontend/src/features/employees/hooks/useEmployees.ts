import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { QUERY_KEYS } from '@/constants/api';
import { employeeApi } from '../api/employee.api';
import type { CreateEmployeeRequest, UpdateEmployeeRequest, EmployeeListParams } from '../types/employee.types';

/**
 * useEmployees — paginated employee list with caching.
 */
export function useEmployees(params: EmployeeListParams = {}) {
  return useQuery({
    queryKey: QUERY_KEYS.users.list(params),
    queryFn:  () => employeeApi.list(params),
    staleTime: 2 * 60 * 1000, // 2 minutes
  });
}

/**
 * useEmployee — single employee detail with 5-minute cache.
 */
export function useEmployee(id: string) {
  return useQuery({
    queryKey: QUERY_KEYS.users.detail(id),
    queryFn:  () => employeeApi.get(id),
    enabled:  !!id,
  });
}

/**
 * useCurrentEmployee — fetches the authenticated user's own profile.
 */
export function useCurrentEmployee() {
  return useQuery({
    queryKey: QUERY_KEYS.users.me,
    queryFn:  () => employeeApi.me(),
    staleTime: 5 * 60 * 1000,
  });
}

/**
 * useCreateEmployee — mutation with optimistic list invalidation.
 */
export function useCreateEmployee() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: CreateEmployeeRequest) => employeeApi.create(data),
    onSuccess: () => {
      void qc.invalidateQueries({ queryKey: QUERY_KEYS.users.all });
    },
  });
}

/**
 * useUpdateEmployee — optimistic update: patches cache immediately,
 * then invalidates on settle to sync with server truth.
 */
export function useUpdateEmployee(id: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: UpdateEmployeeRequest) => employeeApi.update(id, data),
    onMutate: async (data) => {
      await qc.cancelQueries({ queryKey: QUERY_KEYS.users.detail(id) });
      const previous = qc.getQueryData(QUERY_KEYS.users.detail(id));
      qc.setQueryData(QUERY_KEYS.users.detail(id), (old: unknown) =>
        old && typeof old === 'object' ? { ...old, ...data } : old
      );
      return { previous };
    },
    onError: (_err, _vars, context) => {
      if (context?.previous !== undefined) {
        qc.setQueryData(QUERY_KEYS.users.detail(id), context.previous);
      }
    },
    onSettled: () => {
      void qc.invalidateQueries({ queryKey: QUERY_KEYS.users.detail(id) });
      void qc.invalidateQueries({ queryKey: QUERY_KEYS.users.all });
    },
  });
}
