import { useMemo } from 'react';
import { motion } from 'framer-motion';
import { Users, Target, Activity, Calendar, Zap, ArrowRight, UserCheck } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { staggerContainer, slideUpVariants, cardTransition, hoverScale, tapScale } from '@/components/motion/variants';
import { useDashboardKPIs, useRecentActivity } from '@/features/dashboard/hooks/useDashboard';
import { Link } from 'react-router-dom';
import { ROUTES } from '@/constants/routes';
import { formatDistanceToNow } from 'date-fns';

export function ManagerDashboard() {
  const { data: kpis, isLoading: isLoadingKpis } = useDashboardKPIs();
  const { data: activities, isLoading: isLoadingActivity } = useRecentActivity(5);

  const metrics = useMemo(() => {
    return [
      { title: 'Team Members', value: '12', icon: Users },
      { title: 'Pending Reviews', value: kpis?.pendingApprovals?.toString() || '—', icon: Target },
      { title: 'Completed (Month)', value: kpis?.completedThisMonth?.toString() || '—', icon: Zap },
      { title: 'Bias Alerts', value: '3', icon: Activity },
    ];
  }, [kpis]);

  return (
    <motion.div variants={staggerContainer} initial="hidden" animate="visible" className="space-y-10 pb-12">
      <motion.div variants={slideUpVariants} className="flex flex-col md:flex-row justify-between items-start md:items-end gap-5 border-b border-border pb-6">
        <div className="space-y-1.5">
          <h2 className="text-heading-xl tracking-tight text-foreground">Team Performance</h2>
          <p className="text-body text-muted-foreground max-w-2xl">
            Monitor your team's review cycles, pending approvals, and AI-detected bias alerts.
          </p>
        </div>
      </motion.div>

      {/* KPI Grid */}
      <div className="grid gap-5 grid-cols-1 sm:grid-cols-2 lg:grid-cols-4">
        {isLoadingKpis
          ? Array.from({ length: 4 }).map((_, i) => (
              <div key={i} className="h-32 rounded-xl border border-border bg-surface shadow-sm animate-pulse" />
            ))
          : metrics.map((metric, i) => (
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
            ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <motion.div variants={slideUpVariants} className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
             <h3 className="text-heading-md tracking-tight text-foreground">Pending Approvals</h3>
             <Button variant="ghost" size="sm" asChild>
                <Link to={ROUTES.REVIEWS}>View All</Link>
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
                <h4 className="text-heading-sm text-foreground">No pending approvals</h4>
                <p className="text-body text-muted-foreground max-w-sm mx-auto">
                  You have no review cycles waiting for your approval.
                </p>
              </div>
            ) : (
              activities?.map((item) => (
                <motion.div key={item.id} variants={cardTransition} className="group flex flex-col md:flex-row md:items-center justify-between gap-4 p-5 rounded-xl border border-border bg-surface hover:border-primary/30 transition-colors shadow-sm">
                  <div className="space-y-1.5">
                    <span className="font-semibold text-body text-foreground">{item.title}</span>
                    <p className="text-caption text-muted-foreground leading-relaxed">
                      Updated {formatDistanceToNow(new Date(item.updated_at), { addSuffix: true })}
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

        <motion.div variants={slideUpVariants} className="space-y-4">
           <h3 className="text-heading-md tracking-tight text-foreground">Quick Actions</h3>
           <div className="flex flex-col gap-3">
              <Button variant="outline" className="justify-start" asChild>
                <Link to={ROUTES.REVIEW_CREATE}><Target className="mr-2 h-4 w-4" /> New Review Cycle</Link>
              </Button>
              <Button variant="outline" className="justify-start" asChild>
                <Link to={ROUTES.EMPLOYEES}><UserCheck className="mr-2 h-4 w-4" /> View My Team</Link>
              </Button>
              <Button variant="outline" className="justify-start"><Calendar className="mr-2 h-4 w-4" /> Schedule 1:1</Button>
           </div>
        </motion.div>
      </div>
    </motion.div>
  );
}
