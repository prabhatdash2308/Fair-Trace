/**
 * API endpoint constants.
 * Never construct API paths inline — always use these.
 */
export const API_ENDPOINTS = {
  // Auth
  AUTH: {
    LOGIN: '/auth/login',
    LOGOUT: '/auth/logout',
    REFRESH: '/auth/refresh',
    ME: '/auth/me',
  },

  // Users
  USERS: {
    LIST: '/users',
    CREATE: '/users',
    GET: (id: string) => `/users/${id}`,
    UPDATE: (id: string) => `/users/${id}`,
    DELETE: (id: string) => `/users/${id}`,
    ME: '/users/me',
  },

  // Review Cycles
  CYCLES: {
    LIST: '/review-cycles',
    CREATE: '/review-cycles',
    GET: (id: string) => `/review-cycles/${id}`,
    STATUS: (id: string) => `/review-cycles/${id}/status`,
    INPUTS: (id: string) => `/review-cycles/${id}/inputs`,
    TRIGGER: (id: string) => `/review-cycles/${id}/pipeline/trigger`,
  },

  // Pipeline
  PIPELINE: {
    STATUS: (runId: string) => `/pipeline/${runId}/status`,
  },

  // Reports
  REPORTS: {
    GET: (id: string) => `/reports/${id}`,
    STATUS: (id: string) => `/reports/${id}/status`,
    VERSIONS: (id: string) => `/reports/${id}/versions`,
  },

  // Audit
  AUDIT: {
    LIST: '/audit',
    RESOURCE: (type: string, id: string) => `/audit/resource/${type}/${id}`,
    PIPELINE: (runId: string) => `/audit/pipeline/${runId}`,
  },
} as const;
