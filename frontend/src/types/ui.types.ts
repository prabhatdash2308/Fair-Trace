import type { LucideIcon } from 'lucide-react';
import type { VariantProps } from 'class-variance-authority';

/**
 * Shared UI component prop types.
 */

export interface BaseComponentProps {
  className?: string;
  children?: React.ReactNode;
}

export interface NavItem {
  name: string;
  href: string;
  icon: LucideIcon;
  badge?: string | number;
  requiredRole?: string;
}

export interface BreadcrumbItem {
  label: string;
  href?: string;
}

export interface MetricCardProps {
  title: string;
  value: string | number;
  description?: string;
  icon?: LucideIcon;
  trend?: {
    value: number;
    direction: 'up' | 'down' | 'neutral';
    label?: string;
  };
  variant?: 'default' | 'success' | 'warning' | 'danger' | 'info';
  loading?: boolean;
  className?: string;
}

export interface PageHeaderProps {
  title: string;
  subtitle?: string;
  actions?: React.ReactNode;
  breadcrumbs?: BreadcrumbItem[];
  className?: string;
}

export interface SectionHeaderProps {
  title: string;
  description?: string;
  badge?: string;
  actions?: React.ReactNode;
  className?: string;
}

export interface LoadingStateProps {
  text?: string;
  rows?: number;
  className?: string;
}

export interface EmptyStateProps {
  icon?: LucideIcon;
  title: string;
  description?: string;
  action?: {
    label: string;
    onClick: () => void;
  };
  className?: string;
}

export interface ErrorStateProps {
  title?: string;
  message?: string;
  onRetry?: () => void;
  className?: string;
}

export type { VariantProps };
