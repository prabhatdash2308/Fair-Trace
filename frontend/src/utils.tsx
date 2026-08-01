// Shared UI utility functions

import React from 'react'

export function statusBadge(status: string): React.ReactElement {
  const map: Record<string, { cls: string; label: string }> = {
    DRAFT: { cls: 'badge-gray', label: 'Draft' },
    ACTIVE: { cls: 'badge-blue', label: 'Active' },
    PROCESSING: { cls: 'badge-purple', label: 'Processing' },
    PENDING_APPROVAL: { cls: 'badge-yellow', label: 'Pending Approval' },
    COMPLETED: { cls: 'badge-green', label: 'Completed' },
    CANCELLED: { cls: 'badge-red', label: 'Cancelled' },
    FINALIZED: { cls: 'badge-green', label: 'Finalized' },
    REVISION_REQUESTED: { cls: 'badge-yellow', label: 'Revision' },
    REJECTED: { cls: 'badge-red', label: 'Rejected' },
  }
  const { cls, label } = map[status] || { cls: 'badge-gray', label: status }
  return React.createElement('span', { className: `badge ${cls}` }, label)
}

export function confidenceBadge(level: string): string {
  return level === 'HIGH' ? 'badge-green' :
    level === 'MEDIUM' ? 'badge-blue' :
    level === 'LOW' ? 'badge-yellow' : 'badge-red'
}

export function biasSeverityColor(severity: string): string {
  return severity === 'HIGH' ? '#fca5a5' : severity === 'MEDIUM' ? '#fcd34d' : '#6ee7b7'
}

export function formatDate(dateStr: string): string {
  if (!dateStr) return '—'
  try { return new Date(dateStr).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' }) }
  catch { return dateStr }
}

export function truncate(str: string, n = 80): string {
  return str.length > n ? str.slice(0, n) + '...' : str
}
