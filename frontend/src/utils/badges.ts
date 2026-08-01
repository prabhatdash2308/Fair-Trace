import { cn } from '@/lib/utils';
import type { CycleStatus, ReportStatus, ConfidenceLevel, Severity, PipelineRunStatus } from '@/types';

/**
 * Badge utility functions.
 * Migrated and typed from src/utils.tsx — returns Tailwind class strings.
 * Use with the shadcn Badge component.
 */

// ── Cycle Status ──────────────────────────────────────────────────────

const CYCLE_STATUS_CLASSES: Record<CycleStatus, string> = {
  DRAFT:            'bg-slate-500/10 text-slate-500 border-slate-500/20',
  ACTIVE:           'bg-blue-500/10 text-blue-500 border-blue-500/20',
  PROCESSING:       'bg-purple-500/10 text-purple-500 border-purple-500/20',
  PENDING_APPROVAL: 'bg-amber-500/10 text-amber-600 border-amber-500/20',
  COMPLETED:        'bg-emerald-500/10 text-emerald-600 border-emerald-500/20',
  CANCELLED:        'bg-rose-500/10 text-rose-500 border-rose-500/20',
};

export function cycleStatusClasses(status: CycleStatus): string {
  return cn('border', CYCLE_STATUS_CLASSES[status] ?? 'bg-muted text-muted-foreground border-border');
}

// ── Report Status ─────────────────────────────────────────────────────

const REPORT_STATUS_CLASSES: Record<ReportStatus, string> = {
  DRAFT:              'bg-slate-500/10 text-slate-500 border-slate-500/20',
  PENDING_APPROVAL:   'bg-amber-500/10 text-amber-600 border-amber-500/20',
  FINALIZED:          'bg-emerald-500/10 text-emerald-600 border-emerald-500/20',
  REVISION_REQUESTED: 'bg-orange-500/10 text-orange-600 border-orange-500/20',
  REJECTED:           'bg-rose-500/10 text-rose-500 border-rose-500/20',
};

export function reportStatusClasses(status: ReportStatus): string {
  return cn('border', REPORT_STATUS_CLASSES[status] ?? 'bg-muted text-muted-foreground border-border');
}

// ── Confidence Level ──────────────────────────────────────────────────

const CONFIDENCE_CLASSES: Record<ConfidenceLevel, string> = {
  HIGH:         'bg-emerald-500/10 text-emerald-600 border-emerald-500/20',
  MEDIUM:       'bg-blue-500/10 text-blue-500 border-blue-500/20',
  LOW:          'bg-amber-500/10 text-amber-600 border-amber-500/20',
  INSUFFICIENT: 'bg-rose-500/10 text-rose-500 border-rose-500/20',
};

export function confidenceClasses(level: ConfidenceLevel): string {
  return cn('border', CONFIDENCE_CLASSES[level] ?? 'bg-muted text-muted-foreground border-border');
}

// ── Severity ──────────────────────────────────────────────────────────

const SEVERITY_CLASSES: Record<Severity, string> = {
  HIGH:   'bg-rose-500/10 text-rose-600 border-rose-500/20',
  MEDIUM: 'bg-amber-500/10 text-amber-600 border-amber-500/20',
  LOW:    'bg-slate-500/10 text-slate-500 border-slate-500/20',
};

export function severityClasses(severity: Severity): string {
  return cn('border', SEVERITY_CLASSES[severity] ?? 'bg-muted text-muted-foreground border-border');
}

// ── Pipeline Status ───────────────────────────────────────────────────

const PIPELINE_STATUS_CLASSES: Record<PipelineRunStatus, string> = {
  PENDING:   'bg-slate-500/10 text-slate-500 border-slate-500/20',
  RUNNING:   'bg-blue-500/10 text-blue-500 border-blue-500/20',
  COMPLETED: 'bg-emerald-500/10 text-emerald-600 border-emerald-500/20',
  FAILED:    'bg-rose-500/10 text-rose-600 border-rose-500/20',
  HALTED:    'bg-amber-500/10 text-amber-600 border-amber-500/20',
};

export function pipelineStatusClasses(status: PipelineRunStatus): string {
  return cn('border', PIPELINE_STATUS_CLASSES[status] ?? 'bg-muted text-muted-foreground border-border');
}

/** Colour for bias severity — used in chart/canvas contexts where classes won't work. */
export function biasSeverityColor(severity: Severity): string {
  const map: Record<Severity, string> = {
    HIGH: '#F43F5E',
    MEDIUM: '#F59E0B',
    LOW: '#64748B',
  };
  return map[severity] ?? '#64748B';
}
