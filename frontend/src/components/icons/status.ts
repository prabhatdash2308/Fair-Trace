import {
  CheckCircle2,
  XCircle,
  AlertCircle,
  AlertTriangle,
  Info,
  Clock,
  HelpCircle,
  ShieldAlert,
  ShieldCheck,
  Shield
} from 'lucide-react';

export const StatusIcons = {
  Success: CheckCircle2,
  Error: XCircle,
  Warning: AlertTriangle,
  Info,
  Pending: Clock,
  Unknown: HelpCircle,
  Critical: AlertCircle,
  ShieldAlert,
  ShieldCheck,
  Shield,
} as const;
