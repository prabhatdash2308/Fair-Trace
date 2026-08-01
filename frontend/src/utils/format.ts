/**
 * Date and string formatting utilities.
 * Migrated and extended from src/utils.tsx.
 */

/**
 * Formats an ISO date string into a human-readable date.
 * @example formatDate("2024-01-15T10:30:00Z") → "Jan 15, 2024"
 */
export function formatDate(dateStr: string | null | undefined): string {
  if (!dateStr) return '—';
  try {
    return new Date(dateStr).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  } catch {
    return dateStr;
  }
}

/**
 * Formats an ISO date string into a date + time string.
 * @example formatDateTime("2024-01-15T10:30:00Z") → "Jan 15, 2024, 10:30 AM"
 */
export function formatDateTime(dateStr: string | null | undefined): string {
  if (!dateStr) return '—';
  try {
    return new Date(dateStr).toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  } catch {
    return dateStr;
  }
}

/**
 * Returns a relative time string (e.g. "3 minutes ago").
 */
export function formatRelativeTime(dateStr: string | null | undefined): string {
  if (!dateStr) return '—';
  try {
    const diff = Date.now() - new Date(dateStr).getTime();
    const seconds = Math.floor(diff / 1000);
    if (seconds < 60) return 'just now';
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
    return `${Math.floor(seconds / 86400)}d ago`;
  } catch {
    return dateStr;
  }
}

/**
 * Truncates a string to n characters with an ellipsis.
 */
export function truncate(str: string, n = 80): string {
  return str.length > n ? `${str.slice(0, n)}…` : str;
}

/**
 * Formats a number as USD currency.
 * @example formatCurrency(1234.56) → "$1,234.56"
 */
export function formatCurrency(value: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
  }).format(value);
}

/**
 * Formats a number with comma separators.
 * @example formatNumber(1234567) → "1,234,567"
 */
export function formatNumber(value: number): string {
  return new Intl.NumberFormat('en-US').format(value);
}

/**
 * Converts milliseconds to a human-readable duration string.
 * @example formatDuration(3662000) → "1h 1m 2s"
 */
export function formatDuration(ms: number): string {
  const seconds = Math.floor(ms / 1000);
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;
  const parts: string[] = [];
  if (h) parts.push(`${h}h`);
  if (m) parts.push(`${m}m`);
  if (s || !parts.length) parts.push(`${s}s`);
  return parts.join(' ');
}

/**
 * Converts a snake_case or SCREAMING_CASE string to Title Case.
 * @example toTitleCase("PENDING_APPROVAL") → "Pending Approval"
 */
export function toTitleCase(str: string): string {
  return str
    .toLowerCase()
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (c) => c.toUpperCase());
}
