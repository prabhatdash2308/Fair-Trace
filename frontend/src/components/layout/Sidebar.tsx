import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Users,
  LineChart,
  FileText,
  Settings,
  Target,
  ChevronLeft,
  ChevronRight,
  ShieldCheck,
  Activity,
  CheckSquare,
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '@/lib/utils';
import { ROUTES } from '@/constants/routes';
import { THEME_CONSTANTS } from '@/constants/theme';
import type { NavItem } from '@/types/ui.types';

interface SidebarProps {
  isOpen: boolean;
  setIsOpen: (isOpen: boolean) => void;
}

const navItems: NavItem[] = [
  { name: 'Dashboard', href: ROUTES.DASHBOARD, icon: LayoutDashboard },
  { name: 'Employees', href: ROUTES.EMPLOYEES, icon: Users },
  { name: 'Review Cycles', href: ROUTES.REVIEWS, icon: Target },
  { name: 'AI Insights', href: ROUTES.INSIGHTS, icon: LineChart },
  { name: 'Pipeline', href: ROUTES.PIPELINE, icon: Activity },
  { name: 'Reports', href: ROUTES.REPORTS, icon: FileText },
  { name: 'Approvals', href: ROUTES.APPROVALS, icon: CheckSquare },
  { name: 'Settings', href: ROUTES.SETTINGS, icon: Settings },
];

const { OPEN_WIDTH, COLLAPSED_WIDTH, TRANSITION_DURATION } = THEME_CONSTANTS.SIDEBAR;

export function Sidebar({ isOpen, setIsOpen }: SidebarProps) {
  return (
    <motion.aside
      id="app-sidebar"
      initial={false}
      animate={{ width: isOpen ? OPEN_WIDTH : COLLAPSED_WIDTH }}
      transition={{ duration: TRANSITION_DURATION, ease: THEME_CONSTANTS.ANIMATION.EASE_DEFAULT }}
      className="bg-card border-r border-border h-screen flex flex-col relative z-20 shrink-0 overflow-hidden"
    >
      {/* Brand */}
      <div className="h-16 flex items-center px-4 border-b border-border shrink-0">
        <ShieldCheck className="h-7 w-7 text-primary shrink-0" />
        <AnimatePresence>
          {isOpen && (
            <motion.span
              key="brand-text"
              initial={{ opacity: 0, x: -8 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -8 }}
              transition={{ duration: 0.15 }}
              className="ml-3 font-semibold text-base whitespace-nowrap tracking-tight"
            >
              ReviewGuard <span className="text-primary">AI</span>
            </motion.span>
          )}
        </AnimatePresence>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto py-4 px-2 space-y-0.5" aria-label="Main navigation">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.href}
              to={item.href}
              title={!isOpen ? item.name : undefined}
              className={({ isActive }) =>
                cn(
                  'flex items-center px-3 py-2.5 rounded-md transition-colors group w-full',
                  isActive
                    ? 'bg-primary/10 text-primary font-medium'
                    : 'text-muted-foreground hover:bg-muted hover:text-foreground'
                )
              }
            >
              <Icon className="h-5 w-5 shrink-0" />
              <AnimatePresence>
                {isOpen && (
                  <motion.span
                    key={`label-${item.name}`}
                    initial={{ opacity: 0, x: -4 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0 }}
                    transition={{ duration: 0.12 }}
                    className="ml-3 text-sm truncate"
                  >
                    {item.name}
                  </motion.span>
                )}
              </AnimatePresence>
            </NavLink>
          );
        })}
      </nav>

      {/* Collapse toggle */}
      <div className="p-2 border-t border-border shrink-0">
        <button
          id="sidebar-collapse-btn"
          onClick={() => setIsOpen(!isOpen)}
          className="flex w-full items-center justify-center p-2 rounded-md text-muted-foreground hover:bg-muted hover:text-foreground transition-colors"
          aria-label={isOpen ? 'Collapse sidebar' : 'Expand sidebar'}
        >
          {isOpen ? <ChevronLeft className="h-5 w-5" /> : <ChevronRight className="h-5 w-5" />}
        </button>
      </div>
    </motion.aside>
  );
}
