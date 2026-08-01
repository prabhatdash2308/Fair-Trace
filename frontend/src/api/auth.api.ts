import apiClient from './client';
import { API_ENDPOINTS } from '@/constants/api';
import type { User } from '@/types';

export const authApi = {
  login: (email: string, password: string) =>
    apiClient.post<{ access_token: string; user: User }>(
      API_ENDPOINTS.AUTH.LOGIN,
      { email, password }
    ).then((r) => r.data),

  logout: () =>
    apiClient.post(API_ENDPOINTS.AUTH.LOGOUT).then((r) => r.data),

  me: () =>
    apiClient.get<User>(API_ENDPOINTS.AUTH.ME).then((r) => r.data),
};
