/**
 * Employee / User feature types.
 * Mirrors: backend/models/schemas.py — UserResponse, UserCreate, UserUpdate
 *          backend/models/enums.py   — UserRole
 */

export type UserRole = 'ADMIN' | 'MANAGER' | 'EMPLOYEE';

export interface Employee {
  id: string;
  email: string;
  full_name: string;
  role: UserRole;
  manager_id: string | null;
  department?: string;
  designation?: string;
  is_active: boolean;
  created_at: string; // ISO 8601
}

export interface EmployeeListResponse {
  items: Employee[];
  total: number;
  skip: number;
  limit: number;
  has_more: boolean;
}

export interface CreateEmployeeRequest {
  email: string;
  password: string;
  full_name: string;
  role: UserRole;
  manager_id?: string | null;
}

export interface UpdateEmployeeRequest {
  full_name?: string;
  is_active?: boolean;
  manager_id?: string | null;
}

export interface EmployeeListParams {
  skip?: number;
  limit?: number;
}
