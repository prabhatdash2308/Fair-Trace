import apiClient from '@/api/client';
import { API_ENDPOINTS } from '@/constants/api';
import type {
  Employee,
  EmployeeListResponse,
  CreateEmployeeRequest,
  UpdateEmployeeRequest,
  EmployeeListParams,
} from '../types/employee.types';

export const employeeApi = {
  list: (params: EmployeeListParams = {}) =>
    apiClient
      .get<EmployeeListResponse>(API_ENDPOINTS.USERS.LIST, { params })
      .then((r) => r.data),

  get: (id: string) =>
    apiClient
      .get<Employee>(API_ENDPOINTS.USERS.GET(id))
      .then((r) => r.data),

  create: (data: CreateEmployeeRequest) =>
    apiClient
      .post<Employee>(API_ENDPOINTS.USERS.CREATE, data)
      .then((r) => r.data),

  update: (id: string, data: UpdateEmployeeRequest) =>
    apiClient
      .patch<Employee>(API_ENDPOINTS.USERS.UPDATE(id), data)
      .then((r) => r.data),

  me: () =>
    apiClient
      .get<Employee>(API_ENDPOINTS.USERS.ME)
      .then((r) => r.data),
};
