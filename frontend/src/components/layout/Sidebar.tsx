import { useEffect } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import {
  LayoutDashboard, Users, LineChart, FileText, Settings, Target,
  ChevronLeft, ChevronRight, ShieldCheck, Activity, LogOut, Building, User,
  Shield, BookOpen, Award, CheckSquare, History
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '@/lib/utils';
import { ROUTES } from '@/constants/routes';
import { THEME_CONSTANTS } from '@/constants/theme';
import { useAuthStore } from '@/store/auth/auth.store';
import { authService } from '@/features/auth/services/auth.service';
import { ROLE_LABELS } from '@/constants/roles';

interface SidebarProps {
  isOpen: boolean;
  setIsOpen: (isOpen: boolean) => void;
}

const { OPEN_WIDTH, COLLAPSED_WIDTH, TRANSITION_DURATION } = THEME_CONSTANTS.SIDEBAR;

// Generate navigation based on user role
function getNavSections(role: string | undefined) {
  switch (role) {
    case 'ADMIN':
      return [
        {
          label: 'Overview',
          items: [
            { name: 'Dashboard', href: ROUTES.DASHBOARD_ADMIN, icon: LayoutDashboard },
            { name: 'Organizations', href: '#orgs', icon: Building },
            { name: 'Users', href: ROUTES.EMPLOYEES, icon: Users },
            { name: 'Reviews', href: ROUTES.REVIEWS, icon: Target },
            { name: 'Policies', href: '#policies', icon: ShieldCheck },
          ]
        },
        {
          label: 'Administration',
          items: [
            { name: 'Audit Logs', href: '#audit', icon: History },
            { name: 'Analytics', href: ROUTES.REPORTS, icon: LineChart },
            { name: 'Settings', href: ROUTES.SETTINGS, icon: Settings },
            { name: 'Security', href: '#security', icon: Shield },
          ]
        }
      ];
    case 'MANAGER':
      return [
        {
          label: 'Overview',
          items: [
            { name: 'Dashboard', href: ROUTES.DASHBOARD_MANAGER, icon: LayoutDashboard },
            { name: 'My Team', href: ROUTES.EMPLOYEES, icon: Users },
            { name: 'Reviews', href: ROUTES.REVIEWS, icon: Target },
            { name: 'Approvals', href: ROUTES.APPROVALS, icon: CheckSquare },
          ]
        },
        {
          label: 'Analytics',
          items: [
            { name: 'Performance', href: '#perf', icon: LineChart },
            { name: 'Goals', href: '#goals', icon: Target },
            { name: 'Reports', href: ROUTES.REPORTS, icon: FileText },
            { name: 'Settings', href: ROUTES.SETTINGS, icon: Settings },
          ]
        }
      ];
    case 'EMPLOYEE':
    default:
      return [
        {
          label: 'Overview',
          items: [
            { name: 'Dashboard', href: ROUTES.DASHBOARD_EMPLOYEE, icon: LayoutDashboard },
            { name: 'My Reviews', href: ROUTES.REVIEWS, icon: Target },
            { name: 'Goals', href: '#goals', icon: Target },
            { name: 'Feedback', href: '#feedback', icon: FileText },
          ]
        },
        {
          label: 'Career',
          items: [
            { name: 'Career Progress', href: '#career', icon: LineChart },
            { name: 'Achievements', href: '#achievements', icon: Award },
            { name: 'Learning', href: '#learning', icon: BookOpen },
            { name: 'Settings', href: ROUTES.SETTINGS, icon: Settings },
          ]
        }
      ];
  }
}

export function Sidebar({ isOpen, setIsOpen }: SidebarProps) {
  const navigate = useNavigate();
  const user = useAuthStore((state) => state.user);

  // Keyboard shortcut Ctrl+B
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'b') {
        e.preventDefault();
        setIsOpen(!isOpen);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, setIsOpen]);

  const handleLogout = async () => {
    await authService.logout();
    navigate(ROUTES.ROOT);
  };

  const navSections = getNavSections(user?.role);
  const roleLabel = user?.role ? ROLE_LABELS[user.role as keyof typeof ROLE_LABELS] : 'User';

  const renderNavGroup = (items: Array<{ name: string; href: string; icon: React.ElementType }>, label: string) => (
    <div key={label} className="mb-6">
      {isOpen && (
        <div className="px-4 mb-2 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
          {label}
        </div>
      )}
      <div className="space-y-0.5 px-2">
        {items.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.href}
              to={item.href}
              title={!isOpen ? item.name : undefined}
              className={({ isActive }) =>
                cn(
                  'flex items-center px-3 py-2 rounded-md transition-colors group w-full',
                  isActive
                    ? 'bg-primary/10 text-primary font-medium'
                    : 'text-muted-foreground hover:bg-muted hover:text-foreground'
                )
              }
            >
              <Icon className="h-4 w-4 shrink-0" />
              <AnimatePresence>
                {isOpen && (
                  <motion.span
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
      </div>
    </div>
  );

  return (
    <motion.aside
      id="app-sidebar"
      initial={false}
      animate={{ width: isOpen ? OPEN_WIDTH : COLLAPSED_WIDTH }}
      transition={{ duration: TRANSITION_DURATION, ease: THEME_CONSTANTS.ANIMATION.EASE_DEFAULT }}
      className="bg-card border-r border-border h-screen flex flex-col relative z-20 shrink-0 overflow-hidden selection:bg-primary/20 selection:text-primary"
    >
      {/* Brand */}
      <div className="h-16 flex items-center px-4 border-b border-border shrink-0 cursor-pointer" onClick={() => navigate(ROUTES.DASHBOARD)}>
        <ShieldCheck className="h-6 w-6 text-primary shrink-0" />
        <AnimatePresence>
          {isOpen && (
            <motion.span
              key="brand-text"
              initial={{ opacity: 0, x: -8 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -8 }}
              transition={{ duration: 0.15 }}
              className="ml-3 font-semibold text-sm whitespace-nowrap tracking-tight"
            >
              ReviewGuard <span className="text-primary">AI</span>
            </motion.span>
          )}
        </AnimatePresence>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto py-6" aria-label="Main navigation">
        {navSections.map((section) => renderNavGroup(section.items, section.label))}
      </nav>

      {/* Bottom Actions */}
      <div className="p-2 border-t border-border shrink-0 flex flex-col gap-1">
        <button
          onClick={() => {}}
          title={!isOpen ? roleLabel : undefined}
          className="flex items-center px-3 py-2 rounded-md transition-colors text-muted-foreground hover:bg-muted hover:text-foreground w-full"
        >
          <Building className="h-4 w-4 shrink-0" />
          {isOpen && <span className="ml-3 text-sm truncate text-left">{roleLabel}</span>}
        </button>
        <button
          onClick={() => {}}
          title={!isOpen ? "Profile" : undefined}
          className="flex items-center px-3 py-2 rounded-md transition-colors text-muted-foreground hover:bg-muted hover:text-foreground w-full"
        >
          <User className="h-4 w-4 shrink-0" />
          {isOpen && <span className="ml-3 text-sm truncate text-left">{user?.full_name || 'Profile'}</span>}
        </button>
        <button
          onClick={handleLogout}
          title={!isOpen ? "Logout" : undefined}
          className="flex items-center px-3 py-2 rounded-md transition-colors text-muted-foreground hover:bg-destructive/10 hover:text-destructive w-full"
        >
          <LogOut className="h-4 w-4 shrink-0" />
          {isOpen && <span className="ml-3 text-sm truncate text-left">Logout</span>}
        </button>
      </div>

      {/* Collapse toggle */}
      <div className="p-2 border-t border-border shrink-0 bg-muted/30">
        <button
          id="sidebar-collapse-btn"
          onClick={() => setIsOpen(!isOpen)}
          className="flex w-full items-center justify-center p-2 rounded-md text-muted-foreground hover:bg-muted hover:text-foreground transition-colors group"
          aria-label={isOpen ? 'Collapse sidebar (Ctrl+B)' : 'Expand sidebar (Ctrl+B)'}
          title="Toggle Sidebar (Ctrl+B)"
        >
          {isOpen ? <ChevronLeft className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
        </button>
      </div>
    </motion.aside>
  );
}
