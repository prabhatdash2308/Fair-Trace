import { useMemo } from 'react';
import { motion } from 'framer-motion';
import { Users, Target, Activity, Zap, ArrowRight, Lock, Loader2, AlertCircle, Calendar } from "lucide-react";
import { Button } from "@/components/ui/button";
import { APP_CAPABILITIES } from '@/config/capabilities';
import { staggerContainer, slideUpVariants, cardTransition, hoverScale, tapScale } from '@/components/motion/variants';
import { useDashboardKPIs, useRecentActivity } from '@/features/dashboard/hooks/useDashboard.ts';
import { Link } from 'react-router-dom';
import { ROUTES } from '@/constants/routes';
import { formatDistanceToNow } from 'date-fns';

export function Dashboard() {
  const { data: kpis, isLoading: isLoadingKpis, isError: isKpisError } = useDashboardKPIs();
  const { data: activities, isLoading: isLoadingActivity } = useRecentActivity(5);

  const metrics = useMemo(() => {
    if (!kpis) return [];
    return [
      { title: "Total Cycles", value: kpis.totalCycles.toString(), icon: Users },
      { title: "Active Cycles", value: kpis.activeCycles.toString(), icon: Activity },
      { title: "Pending Approvals", value: kpis.pendingApprovals.toString(), icon: Target },
      { title: "Completed (This Month)", value: kpis.completedThisMonth.toString(), icon: Zap },
    ];
  }, [kpis]);

  return (
    <motion.div
      variants={staggerContainer}
      initial="hidden"
      animate="visible"
      className="space-y-10 pb-12"
    >
      <motion.div variants={slideUpVariants} className="flex flex-col md:flex-row justify-between items-start md:items-end gap-5 border-b border-border pb-6">
        <div className="space-y-1.5">
          <h2 className="text-heading-xl tracking-tight text-foreground">Executive Overview</h2>
          <p className="text-body text-muted-foreground max-w-2xl">
            Real-time telemetry of workforce performance, AI decisions, and enterprise risk vectors.
          </p>
        </div>
        
        <Button 
          variant="outline" 
          className="gap-2 shrink-0 transition-colors shadow-sm group"
          disabled={!APP_CAPABILITIES.reports.exportPDF}
          title={!APP_CAPABILITIES.reports.exportPDF ? "Report export is disabled by your organization" : "Download Executive Report"}
        >
          {!APP_CAPABILITIES.reports.exportPDF && <Lock className="h-4 w-4 text-muted-foreground mr-1" />}
          Download Executive Report <ArrowRight className="h-4 w-4 opacity-70 group-hover:translate-x-1 transition-transform" />
        </Button>
      </motion.div>

      {/* Primary Metrics Grid */}
      <div className="grid gap-5 grid-cols-1 sm:grid-cols-2 lg:grid-cols-4">
        {isLoadingKpis ? (
          // Skeletons
          Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="h-32 rounded-xl border border-border bg-surface shadow-sm animate-pulse" />
          ))
        ) : isKpisError ? (
          <div className="col-span-1 sm:col-span-2 lg:col-span-4 p-6 rounded-xl border border-danger/30 bg-danger/10 flex items-center gap-3 text-danger">
            <AlertCircle className="h-5 w-5" />
            <span className="text-sm font-medium">Unable to load dashboard metrics.</span>
          </div>
        ) : (
          metrics.map((metric, i) => (
            <motion.div key={i} variants={cardTransition} whileHover={hoverScale} whileTap={tapScale}>
              <div className="flex flex-col gap-4 p-6 rounded-xl border border-border bg-surface hover:bg-muted/30 transition-colors shadow-sm">
                <div className="flex items-center justify-between">
                  <span className="text-caption font-semibold text-muted-foreground uppercase tracking-widest">{metric.title}</span>
                  <metric.icon className="h-4 w-4 text-muted-foreground opacity-60" />
                </div>
                <div className="flex items-end justify-between">
                  <span className="text-heading-lg tracking-tight text-foreground leading-none">{metric.value}</span>
                </div>
              </div>
            </motion.div>
          ))
        )}
      </div>

      {/* Action Items List */}
      <motion.div variants={slideUpVariants} className="pt-2">
        <div className="flex items-center justify-between mb-5">
          <h3 className="text-heading-md tracking-tight text-foreground">Recent Activity</h3>
          <Button variant="ghost" size="sm" className="text-body font-medium text-muted-foreground hover:text-foreground" asChild>
            <Link to={ROUTES.REVIEWS}>View all cycles</Link>
          </Button>
        </div>
        
        <div className="flex flex-col gap-3">
          {isLoadingActivity ? (
            Array.from({ length: 3 }).map((_, i) => (
              <div key={i} className="h-20 rounded-xl border border-border bg-surface shadow-sm animate-pulse" />
            ))
          ) : activities?.length === 0 ? (
            <div className="p-12 border border-dashed border-border rounded-xl text-center space-y-3 bg-surface-secondary">
              <div className="w-12 h-12 rounded-full bg-surface border border-border flex items-center justify-center mx-auto mb-4">
                <Calendar className="h-5 w-5 text-muted-foreground" />
              </div>
              <h4 className="text-heading-sm text-foreground">No recent activity</h4>
              <p className="text-body text-muted-foreground max-w-sm mx-auto">
                No review cycles have been modified recently. Start a new evaluation cycle to see activity here.
              </p>
              <Button variant="outline" className="mt-4" asChild>
                <Link to={ROUTES.REVIEWS}>Manage Cycles</Link>
              </Button>
            </div>
          ) : (
            activities?.map((item) => (
              <motion.div key={item.id} variants={cardTransition} className="group flex flex-col md:flex-row md:items-center justify-between gap-4 p-5 rounded-xl border border-border bg-surface hover:border-primary/30 transition-colors shadow-sm">
                <div className="space-y-1.5">
                  <span className="font-semibold text-body text-foreground">{item.title}</span>
                  <p className="text-caption text-muted-foreground leading-relaxed">
                    Last updated {formatDistanceToNow(new Date(item.updated_at), { addSuffix: true })}
                  </p>
                </div>
                <div className="flex items-center gap-4 shrink-0 mt-2 md:mt-0">
                  <span className={`inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-semibold ${
                    item.status === 'ACTIVE' ? 'bg-primary/10 text-primary border-primary/20' : 
                    item.status === 'COMPLETED' ? 'bg-success/10 text-success border-success/20' : 
                    'bg-warning/10 text-warning border-warning/20'
                  }`}>
                    {item.status}
                  </span>
                  <Button variant="ghost" size="icon" className="h-8 w-8 text-muted-foreground md:opacity-0 md:group-hover:opacity-100 transition-opacity" asChild>
                    <Link to={`${ROUTES.REVIEWS}/${item.id}`}>
                      <ArrowRight className="h-4 w-4" />
                    </Link>
                  </Button>
                </div>
              </motion.div>
            ))
          )}
        </div>
      </motion.div>
    </motion.div>
  );
}

