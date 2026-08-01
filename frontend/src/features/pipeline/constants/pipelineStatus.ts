import { CheckCircle2, Clock, XCircle, Loader2, AlertCircle, PlayCircle, type LucideIcon } from 'lucide-react';
import type { AgentStatus, PipelineStatus } from '../types/pipeline.types';

export type NormalizedStatus = 'PENDING' | 'RUNNING' | 'COMPLETED' | 'FAILED' | 'WAITING' | 'SKIPPED';

export interface StatusConfig {
  label: string;
  icon: LucideIcon;
  color: string;       // e.g., 'text-success' or custom hex
  bg: string;          // e.g., 'bg-success/10'
  progress: number;    // 0-100 logic or arbitrary
  animation?: string;  // e.g., 'animate-spin'
}

export const PIPELINE_STATUS_MAP: Record<NormalizedStatus, StatusConfig> = {
  PENDING: {
    label: 'Pending',
    icon: Clock,
    color: 'text-muted-foreground',
    bg: 'bg-muted',
    progress: 0,
  },
  RUNNING: {
    label: 'Running',
    icon: Loader2,
    color: 'text-blue-500',
    bg: 'bg-blue-500/10',
    progress: 50,
    animation: 'animate-spin',
  },
  COMPLETED: {
    label: 'Completed',
    icon: CheckCircle2,
    color: 'text-success',
    bg: 'bg-success/10',
    progress: 100,
  },
  FAILED: {
    label: 'Failed',
    icon: XCircle,
    color: 'text-destructive',
    bg: 'bg-destructive/10',
    progress: 100,
  },
  WAITING: {
    label: 'Waiting Approval',
    icon: AlertCircle,
    color: 'text-warning-foreground',
    bg: 'bg-warning/20',
    progress: 75,
  },
  SKIPPED: {
    label: 'Skipped',
    icon: PlayCircle,
    color: 'text-muted-foreground',
    bg: 'bg-muted/50',
    progress: 100,
  }
};

// Helper to map backend PipelineStatus to NormalizedStatus
export const normalizePipelineStatus = (status: PipelineStatus): NormalizedStatus => {
  switch (status) {
    case 'QUEUED': return 'PENDING';
    case 'RUNNING': return 'RUNNING';
    case 'COMPLETED': return 'COMPLETED';
    case 'FAILED': return 'FAILED';
    case 'HALTED': return 'WAITING'; // Often implies waiting for human input in LangGraph
    default: return 'PENDING';
  }
};

// Helper to map backend AgentStatus to NormalizedStatus
export const normalizeAgentStatus = (status: AgentStatus): NormalizedStatus => {
  switch (status) {
    case 'PENDING': return 'PENDING';
    case 'RUNNING': return 'RUNNING';
    case 'COMPLETED': return 'COMPLETED';
    case 'FAILED': return 'FAILED';
    case 'SKIPPED': return 'SKIPPED';
    default: return 'PENDING';
  }
};
