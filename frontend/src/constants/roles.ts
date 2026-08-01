/**
 * User roles — mirrors the backend UserRole enum.
 */
export const ROLES = {
  ADMIN: 'ADMIN',
  MANAGER: 'MANAGER',
  EMPLOYEE: 'EMPLOYEE',
} as const;

export type Role = (typeof ROLES)[keyof typeof ROLES];

/**
 * Role display labels.
 */
export const ROLE_LABELS: Record<Role, string> = {
  ADMIN: 'Administrator',
  MANAGER: 'Manager',
  EMPLOYEE: 'Employee',
};

/**
 * Role hierarchy — higher value = more authority.
 * Used in guards to check minimum required role.
 */
export const ROLE_HIERARCHY: Record<Role, number> = {
  EMPLOYEE: 1,
  MANAGER: 2,
  ADMIN: 3,
};
