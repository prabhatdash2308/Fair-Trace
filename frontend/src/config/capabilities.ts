/**
 * FairTrace - Backend Capability Configuration
 * 
 * Centralized feature flags for adapting the UI based on backend availability 
 * or organizational configuration.
 */

export const APP_CAPABILITIES = {
  auth: {
    sso: {
      google: false,
      microsoft: false,
      github: false,
    },
    forgotPassword: false,
  },
  reports: {
    exportPDF: false,
    exportCSV: false,
    versionComparison: false,
  },
  pipeline: {
    liveExecutionTrace: false,
  },
} as const;
