import { Building, ShieldCheck, History, Shield, LineChart, Target, FileText, Award, BookOpen } from 'lucide-react';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { Button } from '@/components/ui/button';
import { useLocation } from 'react-router-dom';

const ROUTE_META: Record<string, { title: string, description: string, icon: any }> = {
  '/organizations': { title: 'Organizations', description: 'Manage enterprise organizational units and hierarchies.', icon: Building },
  '/policies': { title: 'Policies', description: 'Configure review policies and compliance rules.', icon: ShieldCheck },
  '/audit-logs': { title: 'Audit Logs', description: 'View immutable system activity and security events.', icon: History },
  '/security': { title: 'Security Settings', description: 'Manage RBAC, SSO, and platform security.', icon: Shield },
  '/performance': { title: 'Performance Analytics', description: 'Track team and organizational performance metrics.', icon: LineChart },
  '/goals': { title: 'Goals', description: 'Set and track OKRs and performance goals.', icon: Target },
  '/feedback': { title: 'Continuous Feedback', description: 'Provide and request real-time feedback.', icon: FileText },
  '/career': { title: 'Career Progress', description: 'Track your career trajectory and milestones.', icon: LineChart },
  '/achievements': { title: 'Achievements', description: 'View your badges, awards, and recognitions.', icon: Award },
  '/learning': { title: 'Learning & Development', description: 'Access training materials and growth opportunities.', icon: BookOpen },
};

export function PlaceholderPage() {
  const location = useLocation();
  const meta = ROUTE_META[location.pathname] || { title: 'Coming Soon', description: 'This feature is currently under development.', icon: Target };
  const Icon = meta.icon;

  useDocumentTitle(meta.title);

  return (
    <div className="flex-1 flex flex-col items-center justify-center min-h-[60vh] p-8 text-center animate-in fade-in duration-500">
      <div className="h-20 w-20 bg-primary/10 rounded-3xl flex items-center justify-center mb-6 border border-primary/20 shadow-sm">
        <Icon className="h-10 w-10 text-primary opacity-80" aria-hidden="true" />
      </div>
      <h1 className="text-3xl font-bold tracking-tight text-foreground mb-3">{meta.title}</h1>
      <p className="text-muted-foreground max-w-[460px] text-lg mb-8 leading-relaxed">
        {meta.description}
      </p>
      
      <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-muted/50 border border-border text-sm font-medium text-muted-foreground">
        <span className="relative flex h-2.5 w-2.5 mr-1">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary/60 opacity-75"></span>
          <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-primary"></span>
        </span>
        Backend Integration Pending
      </div>
    </div>
  );
}
