import { Link, useLocation } from 'react-router-dom';
import { ChevronRight, Home } from 'lucide-react';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

/**
 * Route label overrides — customize how path segments appear in breadcrumbs.
 */
const SEGMENT_LABELS: Record<string, string> = {
  dashboard: 'Dashboard',
  employees: 'Employees',
  reviews: 'Review Cycles',
  insights: 'AI Insights',
  reports: 'Reports',
  approvals: 'Approvals',
  pipeline: 'Pipeline',
  settings: 'Settings',
  create: 'Create New',
};

function formatSegment(segment: string): string {
  return SEGMENT_LABELS[segment] ?? segment.replace(/-/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
}

export function Breadcrumbs() {
  const { pathname } = useLocation();
  const segments = pathname.split('/').filter(Boolean);

  if (segments.length === 0) return null;

  const crumbs = segments.map((segment, index) => {
    const href = '/' + segments.slice(0, index + 1).join('/');
    const isLast = index === segments.length - 1;
    const label = formatSegment(segment);
    return { label, href, isLast };
  });

  return (
    <motion.nav
      aria-label="breadcrumb"
      initial={{ opacity: 0, y: -4 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.2 }}
      className="flex items-center gap-1 text-sm text-muted-foreground mb-4"
    >
      <Link
        to="/dashboard"
        className="flex items-center hover:text-foreground transition-colors"
        aria-label="Home"
      >
        <Home className="h-3.5 w-3.5" />
      </Link>

      {crumbs.map(({ label, href, isLast }) => (
        <span key={href} className="flex items-center gap-1">
          <ChevronRight className="h-3.5 w-3.5 text-border" />
          {isLast ? (
            <span className="text-foreground font-medium">{label}</span>
          ) : (
            <Link
              to={href}
              className={cn(
                'hover:text-foreground transition-colors',
                isLast && 'text-foreground font-medium pointer-events-none'
              )}
            >
              {label}
            </Link>
          )}
        </span>
      ))}
    </motion.nav>
  );
}
