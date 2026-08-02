/**
 * Application routes — single source of truth.
 * Never hard-code paths in components.
 */
export const ROUTES = {
  // Public
  ROOT: '/',
  LOGIN: '/login',
  FORGOT_PASSWORD: '/forgot-password',

  // Dashboard — role-specific workspaces
  DASHBOARD:          '/dashboard',           // Redirects to role workspace
  DASHBOARD_ADMIN:    '/dashboard/admin',
  DASHBOARD_MANAGER:  '/dashboard/manager',
  DASHBOARD_EMPLOYEE: '/dashboard/employee',

  // Employees
  EMPLOYEES: '/employees',
  EMPLOYEE_PROFILE: '/employees/:id',
  employeeProfile: (id: string) => `/employees/${id}`,

  // Review Cycles
  REVIEWS: '/reviews',
  REVIEW_CREATE: '/reviews/create',
  REVIEW_DETAIL: '/reviews/:id',
  reviewDetail: (id: string) => `/reviews/${id}`,

  // AI Pipeline
  PIPELINE: '/pipeline',
  PIPELINE_HISTORY: '/pipeline/history',
  PIPELINE_MONITOR: '/pipeline/:runId',
  pipelineMonitor: (runId: string) => `/pipeline/${runId}`,

  // Reports
  REPORTS: '/reports',
  REPORT_DETAIL: '/reports/:id',
  reportDetail: (id: string) => `/reports/${id}`,
  EXPLAINABILITY: '/explainability/:reportId',
  explainability: (reportId: string) => `/explainability/${reportId}`,

  // Approvals
  APPROVALS: '/approvals',

  // AI Insights
  INSIGHTS: '/insights',

  // Settings
  SETTINGS: '/settings',

  // Sidebar missing pages
  ORGANIZATIONS: '/organizations',
  POLICCIES: '/policies', // Will rename to POLICIES
  POLICIES: '/policies',
  AUDIT_LOGS: '/audit-logs',
  SECURITY: '/security',
  PERFORMANCE: '/performance',
  GOALS: '/goals',
  FEEDBACK: '/feedback',
  CAREER: '/career',
  ACHIEVEMENTS: '/achievements',
  LEARNING: '/learning',

  // Unauthorized
  UNAUTHORIZED: '/unauthorized',
} as const;

/** Returns the role-specific dashboard route for a given role string. */
export function roleDashboardRoute(role: string | undefined): string {
  switch (role) {
    case 'ADMIN':    return ROUTES.DASHBOARD_ADMIN;
    case 'MANAGER':  return ROUTES.DASHBOARD_MANAGER;
    case 'EMPLOYEE': return ROUTES.DASHBOARD_EMPLOYEE;
    default:         return ROUTES.LOGIN;
  }
}
