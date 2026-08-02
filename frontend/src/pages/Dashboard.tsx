import { useMemo } from 'react';
import { motion } from 'framer-motion';
import {
  Users, Target, Activity, Zap, ArrowRight, Lock, AlertCircle, Calendar
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { APP_CAPABILITIES } from '@/config/capabilities';
import { staggerContainer, slideUpVariants, cardTransition } from '@/components/motion/variants';
import { MetricCard } from '@/components/shared/MetricCard';
import { EmptyState } from '@/components/shared/EmptyState';
import { useDashboardKPIs, useRecentActivity } from '@/features/dashboard/hooks/useDashboard.ts';
import { Link } from 'react-router-dom';
import { ROUTES } from '@/constants/routes';
import { formatDistanceToNow } from 'date-fns';
import { cn } from '@/lib/utils';

const STATUS_BADGE: Record<string, { variant: 'default' | 'success' | 'warning' | 'secondary'; label: string }> = {
  ACTIVE:    { variant: 'default',   label: 'Active'    },
  COMPLETED: { variant: 'success',   label: 'Completed' },
  PENDING:   { variant: 'warning',   label: 'Pending'   },
  DRAFT:     { variant: 'secondary', label: 'Draft'     },
};

export function Dashboard() {
  const { data: kpis, isLoading: isLoadingKpis, isError: isKpisError } = useDashboardKPIs();
  const { data: activities, isLoading: isLoadingActivity } = useRecentActivity(5);

  const metrics = useMemo(() => {
    if (!kpis) return [];
    return [
      {
        title: "Total Cycles",
        value: kpis.totalCycles.toString(),
        icon: Users,
        variant: 'default' as const,
        description: "All time",
      },
      {
        title: "Active Cycles",
        value: kpis.activeCycles.toString(),
        icon: Activity,
        variant: 'info' as const,
        description: "In progress",
        trend: kpis.activeCycles > 0
          ? { direction: 'up' as const, value: kpis.activeCycles, label: 'running' }
          : undefined,
      },
      {
        title: "Pending Approvals",
        value: kpis.pendingApprovals.toString(),
        icon: Target,
        variant: kpis.pendingApprovals > 10 ? 'warning' as const : 'default' as const,
        description: "Awaiting review",
      },
      {
        title: "Completed (Month)",
        value: kpis.completedThisMonth.toString(),
        icon: Zap,
        variant: 'success' as const,
        description: "This month",
        trend: kpis.completedThisMonth > 0
          ? { direction: 'up' as const, value: kpis.completedThisMonth, label: 'this month' }
          : undefined,
      },
    ];
  }, [kpis]);

  return (
    <motion.div
      variants={staggerContainer}
      initial="hidden"
      animate="visible"
      className="space-y-8 pb-12"
    >
      {/* ── Page header inline (no PageHeader component — dashboard has special layout) ── */}
      <motion.div
        variants={slideUpVariants}
        className="flex flex-col md:flex-row justify-between items-start md:items-end gap-5 pb-6 border-b border-border"
      >
        <div className="space-y-1">
          <h1 className="text-heading-xl font-semibold text-foreground tracking-tight">
            Executive Overview
          </h1>
          <p className="text-body text-muted-foreground max-w-2xl">
            Real-time telemetry of workforce performance, AI decisions, and enterprise risk vectors.
          </p>
        </div>

        <Button
          variant="outline"
          size="sm"
          className="gap-2 shrink-0 group"
          disabled={!APP_CAPABILITIES.reports.exportPDF}
          title={!APP_CAPABILITIES.reports.exportPDF ? "Report export is disabled by your organization" : "Download Executive Report"}
        >
          {!APP_CAPABILITIES.reports.exportPDF && (
            <Lock className="h-4 w-4 text-muted-foreground" aria-hidden="true" />
          )}
          Download Report
          <ArrowRight className="h-4 w-4 opacity-70 transition-transform duration-[120ms] group-hover:translate-x-0.5" aria-hidden="true" />
        </Button>
      </motion.div>

      {/* ── KPI Metric Cards ── */}
      <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-4">
        {isLoadingKpis ? (
          Array.from({ length: 4 }).map((_, i) => (
            <MetricCard key={i} title="" value="" loading />
          ))
        ) : isKpisError ? (
          <div className="col-span-full flex items-center gap-3 px-4 py-3 rounded-lg border border-danger/20 bg-danger/8 text-danger">
            <AlertCircle className="h-4 w-4 shrink-0" aria-hidden="true" />
            <span className="text-body font-medium">Unable to load dashboard metrics. Check your connection.</span>
          </div>
        ) : (
          metrics.map((metric, i) => (
            <motion.div key={i} variants={cardTransition}>
              <MetricCard
                title={metric.title}
                value={metric.value}
                icon={metric.icon}
                variant={metric.variant}
                description={metric.description}
                trend={metric.trend}
              />
            </motion.div>
          ))
        )}
      </div>

      {/* ── Recent Activity ── */}
      <motion.div variants={slideUpVariants}>
        <div className="flex items-center justify-between mb-5">
          <h2 className="text-heading-md font-semibold text-foreground">Recent Activity</h2>
          <Button variant="ghost" size="sm" className="text-muted-foreground hover:text-foreground gap-1" asChild>
            <Link to={ROUTES.REVIEWS}>
              View all cycles
              <ArrowRight className="h-3.5 w-3.5" aria-hidden="true" />
            </Link>
          </Button>
        </div>

        <div className="flex flex-col gap-2">
          {isLoadingActivity ? (
            Array.from({ length: 3 }).map((_, i) => (
              <div
                key={i}
                className="h-[72px] rounded-lg border border-border bg-card animate-shimmer"
                style={{ opacity: 1 - i * 0.15 }}
              />
            ))
          ) : !activities || activities.length === 0 ? (
            <div className="rounded-lg border border-border bg-card">
              <EmptyState
                icon={Calendar}
                title="No recent activity"
                description="No review cycles have been modified recently. Start a new evaluation cycle to see activity here."
                action={{
                  label: 'Create Review Cycle',
                  onClick: () => {},
                  variant: 'default',
                }}
                secondaryAction={{
                  label: 'Browse Employees',
                  onClick: () => {},
                  variant: 'ghost',
                }}
                size="md"
              />
            </div>
          ) : (
            activities.map((item) => {
              const statusCfg = STATUS_BADGE[item.status] ?? STATUS_BADGE['DRAFT'];
              return (
                <motion.div
                  key={item.id}
                  variants={cardTransition}
                  className={cn(
                    'group flex flex-col md:flex-row md:items-center justify-between gap-4 px-5 py-4',
                    'rounded-lg border border-border bg-card',
                    'hover:border-border/80 hover:shadow-sm',
                    'transition-all duration-[160ms]',
                  )}
                >
                  <div className="space-y-0.5 min-w-0">
                    <p className="text-body font-medium text-foreground truncate">{item.title}</p>
                    <p className="text-caption text-muted-foreground">
                      Updated {formatDistanceToNow(new Date(item.updated_at), { addSuffix: true })}
                    </p>
                  </div>

                  <div className="flex items-center gap-3 shrink-0">
                    <Badge variant={statusCfg.variant}>
                      {statusCfg.label}
                    </Badge>
                    <Button
                      variant="ghost"
                      size="icon-sm"
                      className="text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity duration-[120ms]"
                      aria-label={`View ${item.title}`}
                      asChild
                    >
                      <Link to={`${ROUTES.REVIEWS}/${item.id}`}>
                        <ArrowRight className="h-4 w-4" aria-hidden="true" />
                      </Link>
                    </Button>
                  </div>
                </motion.div>
              );
            })
          )}
        </div>
      </motion.div>
    </motion.div>
  );
}
