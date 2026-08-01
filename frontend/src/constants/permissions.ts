import type { Role } from './roles';
import { ROLES } from './roles';

/**
 * Feature permissions mapped to the minimum role required.
 * Add new features here — guards read from this object.
 */
export const PERMISSIONS = {
  // Dashboard
  VIEW_DASHBOARD: [ROLES.EMPLOYEE, ROLES.MANAGER, ROLES.ADMIN],

  // Employees
  VIEW_EMPLOYEES: [ROLES.MANAGER, ROLES.ADMIN],
  MANAGE_EMPLOYEES: [ROLES.ADMIN],

  // Review Cycles
  VIEW_REVIEWS: [ROLES.EMPLOYEE, ROLES.MANAGER, ROLES.ADMIN],
  CREATE_REVIEW: [ROLES.MANAGER, ROLES.ADMIN],
  MANAGE_REVIEWS: [ROLES.ADMIN],

  // Pipeline
  VIEW_PIPELINE: [ROLES.MANAGER, ROLES.ADMIN],
  TRIGGER_PIPELINE: [ROLES.MANAGER, ROLES.ADMIN],

  // Reports
  VIEW_REPORTS: [ROLES.EMPLOYEE, ROLES.MANAGER, ROLES.ADMIN],
  APPROVE_REPORTS: [ROLES.MANAGER, ROLES.ADMIN],

  // Settings
  VIEW_SETTINGS: [ROLES.ADMIN],
  MANAGE_SETTINGS: [ROLES.ADMIN],

  // Audit
  VIEW_AUDIT: [ROLES.ADMIN],
} as const satisfies Record<string, Role[]>;

export type Permission = keyof typeof PERMISSIONS;

/**
 * Returns true if the given role has the specified permission.
 */
export function hasPermission(role: Role, permission: Permission): boolean {
  return (PERMISSIONS[permission] as Role[]).includes(role);
}
