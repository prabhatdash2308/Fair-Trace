import apiClient from './client';
import { API_ENDPOINTS } from '@/constants/api';
import type { User, UserRole } from '@/types';

export const employeeApi = {
  list: (params?: { skip?: number; limit?: number }) =>
    apiClient.get<User[]>(API_ENDPOINTS.USERS.LIST, { params }).then((r) => r.data),

  get: (id: string) =>
    apiClient.get<User>(API_ENDPOINTS.USERS.GET(id)).then((r) => r.data),

  create: (data: {
    email: string;
    password: string;
    full_name: string;
    role: UserRole;
    manager_id?: string;
  }) => apiClient.post<User>(API_ENDPOINTS.USERS.CREATE, data).then((r) => r.data),

  update: (id: string, data: Partial<User>) =>
    apiClient.patch<User>(API_ENDPOINTS.USERS.UPDATE(id), data).then((r) => r.data),

  me: () =>
    apiClient.get<User>(API_ENDPOINTS.USERS.ME).then((r) => r.data),
};
