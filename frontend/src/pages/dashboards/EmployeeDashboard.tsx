import { useMemo } from 'react';
import { motion } from 'framer-motion';
import { Target, Activity, Zap, TrendingUp, BookOpen, Award, CheckCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { staggerContainer, slideUpVariants, cardTransition, hoverScale, tapScale } from '@/components/motion/variants';
import { Link } from 'react-router-dom';
import { ROUTES } from '@/constants/routes';

export function EmployeeDashboard() {
  const metrics = useMemo(() => {
    return [
      { title: 'Performance Score', value: '—', icon: TrendingUp },
      { title: 'Active Goals', value: '3', icon: Target },
      { title: 'Recent Feedback', value: '12', icon: Activity },
      { title: 'Achievements', value: '4', icon: Award },
    ];
  }, []);

  return (
    <motion.div variants={staggerContainer} initial="hidden" animate="visible" className="space-y-10 pb-12">
      <motion.div variants={slideUpVariants} className="flex flex-col md:flex-row justify-between items-start md:items-end gap-5 border-b border-border pb-6">
        <div className="space-y-1.5">
          <h2 className="text-heading-xl tracking-tight text-foreground">My Workspace</h2>
          <p className="text-body text-muted-foreground max-w-2xl">
            View your personal performance metrics, goals, and feedback history.
          </p>
        </div>
      </motion.div>

      {/* KPI Grid */}
      <div className="grid gap-5 grid-cols-1 sm:grid-cols-2 lg:grid-cols-2">
        <motion.div variants={cardTransition} whileHover={hoverScale} whileTap={tapScale}>
            <div className="flex flex-col gap-4 p-6 rounded-xl border border-border bg-surface hover:bg-muted/30 transition-colors shadow-sm">
              <div className="flex items-center justify-between">
                <span className="text-caption font-semibold text-muted-foreground uppercase tracking-widest">My Reviews</span>
                <Target className="h-4 w-4 text-muted-foreground opacity-60" />
              </div>
              <div className="flex items-end justify-between">
                <span className="text-heading-lg tracking-tight text-foreground leading-none">
                  <Button variant="link" className="p-0 h-auto text-heading-lg" asChild>
                    <Link to={ROUTES.REVIEWS}>View Reviews</Link>
                  </Button>
                </span>
              </div>
            </div>
          </motion.div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <motion.div variants={slideUpVariants} className="lg:col-span-2 space-y-4">
           <div className="flex items-center justify-between">
              <h3 className="text-heading-md tracking-tight text-foreground">Performance Timeline</h3>
           </div>
           <div className="p-12 border border-dashed border-border rounded-xl text-center space-y-3 bg-surface-secondary">
             <div className="w-12 h-12 rounded-full bg-surface border border-border flex items-center justify-center mx-auto mb-4">
               <TrendingUp className="h-5 w-5 text-muted-foreground" />
             </div>
             <h4 className="text-heading-sm text-foreground">No recent performance data</h4>
             <p className="text-body text-muted-foreground max-w-sm mx-auto">
               Once your manager completes a review cycle, your performance history will appear here.
             </p>
           </div>
        </motion.div>

      </div>
    </motion.div>
  );
}
