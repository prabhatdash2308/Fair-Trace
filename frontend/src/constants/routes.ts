/**
 * Application routes — single source of truth.
 * Never hard-code paths in components.
 */
export const ROUTES = {
  // Public
  ROOT: '/',
  LOGIN: '/login',

  // App (protected)
  DASHBOARD: '/dashboard',

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
  PIPELINE_MONITOR: '/pipeline/:runId',
  pipelineMonitor: (runId: string) => `/pipeline/${runId}`,

  // Reports
  REPORTS: '/reports',
  REPORT_DETAIL: '/reports/:id',
  reportDetail: (id: string) => `/reports/${id}`,

  // Approvals
  APPROVALS: '/approvals',

  // AI Insights
  INSIGHTS: '/insights',

  // Settings
  SETTINGS: '/settings',
} as const;
