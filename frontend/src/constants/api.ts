/**
 * API endpoint constants — mirrors FastAPI router paths exactly.
 * Never construct API paths inline — always use these constants.
 *
 * Last synced with: backend/routers/routers.py
 */
export const API_ENDPOINTS = {
  // ── Auth ───────────────────────────────────────────────────────────
  AUTH: {
    LOGIN:   '/auth/login',
    LOGOUT:  '/auth/logout',
    REFRESH: '/auth/refresh',
    ME:      '/auth/me',
  },

  // ── Users / Employees ──────────────────────────────────────────────
  USERS: {
    LIST:   '/users',
    CREATE: '/users',
    GET:    (id: string) => `/users/${id}`,
    UPDATE: (id: string) => `/users/${id}`,
    DELETE: (id: string) => `/users/${id}`,
    ME:     '/users/me',
  },

  // ── Review Cycles ──────────────────────────────────────────────────
  CYCLES: {
    LIST:    '/review-cycles',
    CREATE:  '/review-cycles',
    GET:     (id: string) => `/review-cycles/${id}`,
    STATUS:  (id: string) => `/review-cycles/${id}/status`,
    INPUTS:  (id: string) => `/review-cycles/${id}/inputs`,
    TRIGGER: (id: string) => `/review-cycles/${id}/pipeline/trigger`,
  },

  // ── Pipeline ───────────────────────────────────────────────────────
  PIPELINE: {
    STATUS: (runId: string) => `/pipeline/${runId}/status`,
  },

  // ── Reports ────────────────────────────────────────────────────────
  REPORTS: {
    GET:      (id: string) => `/reports/${id}`,
    STATUS:   (id: string) => `/reports/${id}/status`,
    VERSIONS: (id: string) => `/reports/${id}/versions`,
  },

  // ── Audit ──────────────────────────────────────────────────────────
  AUDIT: {
    LIST:     '/audit',
    RESOURCE: (type: string, id: string) => `/audit/resource/${type}/${id}`,
    PIPELINE: (runId: string) => `/audit/pipeline/${runId}`,
  },
} as const;

/**
 * Query key factory — centralized, typed cache keys for React Query.
 * Using factory pattern ensures keys are composable and type-safe.
 */
export const QUERY_KEYS = {
  // Users
  users:  {
    all:    ['users']                           as const,
    list:   (params: object) => ['users', 'list', params]  as const,
    detail: (id: string)     => ['users', id]              as const,
    me:     ['users', 'me']                     as const,
  },

  // Review Cycles
  cycles: {
    all:    ['cycles']                          as const,
    list:   (params: object) => ['cycles', 'list', params] as const,
    detail: (id: string)     => ['cycles', id]             as const,
    inputs: (id: string)     => ['cycles', id, 'inputs']   as const,
  },

  // Pipeline
  pipeline: {
    status: (runId: string) => ['pipeline', runId, 'status'] as const,
  },

  // Reports
  reports: {
    detail:   (id: string) => ['reports', id]           as const,
    versions: (id: string) => ['reports', id, 'versions'] as const,
  },

  // Audit
  audit: {
    list:     (params: object) => ['audit', 'list', params]               as const,
    resource: (type: string, id: string) => ['audit', type, id]          as const,
    pipeline: (runId: string)  => ['audit', 'pipeline', runId]           as const,
  },

  // Dashboard (derived — no dedicated endpoint, uses existing data)
  dashboard: {
    summary: ['dashboard', 'summary'] as const,
  },
} as const;
