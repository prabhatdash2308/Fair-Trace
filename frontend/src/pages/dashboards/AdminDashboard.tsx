import { useMemo } from 'react';
import { motion } from 'framer-motion';
import { Users, Target, Activity, Zap, ShieldCheck, Building, Key, ShieldAlert } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { staggerContainer, slideUpVariants, cardTransition, hoverScale, tapScale } from '@/components/motion/variants';
import { useDashboardKPIs } from '@/features/dashboard/hooks/useDashboard';
import { useEmployees } from '@/features/employees/hooks/useEmployees';
export function AdminDashboard() {
  const { data: kpis, isLoading: isKPIsLoading } = useDashboardKPIs();
  const { data: usersData, isLoading: isUsersLoading } = useEmployees({ limit: 1 });

  const metrics = useMemo(() => {
    return [
      { title: 'Users', value: usersData?.total?.toString() || '—', icon: Users },
      { title: 'Review Cycles', value: kpis?.totalCycles?.toString() || '—', icon: Target },
      { title: 'Active Cycles', value: kpis?.activeCycles?.toString() || '—', icon: Activity },
      { title: 'System Health', value: '100%', icon: ShieldCheck },
    ];
  }, [kpis, usersData]);

  const isLoading = isKPIsLoading || isUsersLoading;

  return (
    <motion.div variants={staggerContainer} initial="hidden" animate="visible" className="space-y-10 pb-12">
      <motion.div variants={slideUpVariants} className="flex flex-col md:flex-row justify-between items-start md:items-end gap-5 border-b border-border pb-6">
        <div className="space-y-1.5">
          <h2 className="text-heading-xl tracking-tight text-foreground">Platform Administration</h2>
          <p className="text-body text-muted-foreground max-w-2xl">
            Enterprise command center. Monitor system health, organizations, and global security.
          </p>
        </div>
      </motion.div>

      {/* KPI Grid */}
      <div className="grid gap-5 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
        {isLoading
          ? Array.from({ length: 6 }).map((_, i) => (
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
          <h3 className="text-heading-md tracking-tight text-foreground">Recent Audit Activity</h3>
          <div className="p-12 border border-dashed border-border rounded-xl text-center space-y-3 bg-surface-secondary">
             <div className="w-12 h-12 rounded-full bg-surface border border-border flex items-center justify-center mx-auto mb-4">
               <ShieldAlert className="h-5 w-5 text-muted-foreground" />
             </div>
             <h4 className="text-heading-sm text-foreground">No recent security alerts</h4>
             <p className="text-body text-muted-foreground max-w-sm mx-auto">
               System is operating normally. All security events will be logged here.
             </p>
          </div>
        </motion.div>
        
        <motion.div variants={slideUpVariants} className="space-y-4">
           <h3 className="text-heading-md tracking-tight text-foreground">Quick Actions</h3>
           <div className="flex flex-col gap-3">
              <Button variant="outline" className="justify-start"><Users className="mr-2 h-4 w-4" /> Invite User</Button>
              <Button variant="outline" className="justify-start"><Building className="mr-2 h-4 w-4" /> Create Organization</Button>
              <Button variant="outline" className="justify-start"><Key className="mr-2 h-4 w-4" /> Manage API Keys</Button>
           </div>
        </motion.div>
      </div>
    </motion.div>
  );
}
