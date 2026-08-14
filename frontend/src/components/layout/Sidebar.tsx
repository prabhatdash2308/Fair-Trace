import { useEffect } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import {
  LayoutDashboard, Users, LineChart, FileText, Settings, Target,
  ChevronLeft, ChevronRight, ShieldCheck, Activity, LogOut, Building, User,
  Shield, BookOpen, Award, CheckSquare, History, ChevronsLeft, ChevronsRight
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

function getNavSections(role: string | undefined) {
  switch (role) {
    case 'ADMIN':
      return [
        {
          label: 'Overview',
          items: [
            { name: 'Dashboard',      href: ROUTES.DASHBOARD_ADMIN, icon: LayoutDashboard },
            { name: 'Users',          href: ROUTES.EMPLOYEES,       icon: Users },
            { name: 'Reviews',        href: ROUTES.REVIEWS,         icon: Target },
          ]
        },
        {
          label: 'Administration',
          items: [
            { name: 'Settings',       href: ROUTES.SETTINGS,        icon: Settings },
          ]
        }
      ];
    case 'MANAGER':
      return [
        {
          label: 'Overview',
          items: [
            { name: 'Dashboard',      href: ROUTES.DASHBOARD_MANAGER, icon: LayoutDashboard },
            { name: 'My Team',        href: ROUTES.EMPLOYEES,         icon: Users },
            { name: 'Reviews',        href: ROUTES.REVIEWS,           icon: Target },
          ]
        },
        {
          label: 'Analytics',
          items: [
            { name: 'Settings',       href: ROUTES.SETTINGS,          icon: Settings },
          ]
        }
      ];
    case 'EMPLOYEE':
    default:
      return [
        {
          label: 'Overview',
          items: [
            { name: 'Dashboard',      href: ROUTES.DASHBOARD_EMPLOYEE, icon: LayoutDashboard },
            { name: 'My Reviews',     href: ROUTES.REVIEWS,            icon: Target },
          ]
        },
        {
          label: 'Career',
          items: [
            { name: 'Settings',       href: ROUTES.SETTINGS,          icon: Settings },
          ]
        }
      ];
  }
}

export function Sidebar({ isOpen, setIsOpen }: SidebarProps) {
  const navigate = useNavigate();
  const user = useAuthStore((state) => state.user);

  // Keyboard shortcut Ctrl/Cmd+B
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

  // Generate initials for user avatar
  const initials = user?.full_name
    ? user.full_name.split(' ').map(n => n[0]).slice(0, 2).join('').toUpperCase()
    : 'FT';

  const renderNavItem = (item: { name: string; href: string; icon: React.ElementType }) => {
    const Icon = item.icon;
    return (
      <NavLink
        key={item.href}
        to={item.href}
        title={!isOpen ? item.name : undefined}
        className={({ isActive }) =>
          cn(
            'relative flex items-center gap-2.5 px-3 py-2 rounded-md',
            'text-body transition-colors duration-[120ms] group w-full',
            'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring/50',
            isActive
              ? [
                  'bg-primary/8 text-primary font-medium',
                  // Linear-style left accent bar
                  'before:absolute before:left-0 before:top-1/2 before:-translate-y-1/2',
                  'before:w-0.5 before:h-4 before:rounded-r-full before:bg-primary',
                ]
              : 'text-muted-foreground hover:bg-muted/60 hover:text-foreground'
          )
        }
      >
        <Icon className="h-4 w-4 shrink-0" aria-hidden="true" />
        <AnimatePresence>
          {isOpen && (
            <motion.span
              initial={{ opacity: 0, x: -4 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.12 }}
              className="text-body truncate"
            >
              {item.name}
            </motion.span>
          )}
        </AnimatePresence>
      </NavLink>
    );
  };

  const renderSection = (section: { label: string; items: Array<{ name: string; href: string; icon: React.ElementType }> }) => (
    <div key={section.label} className="mb-5">
      {isOpen && (
        <div className="px-3 mb-1.5">
          <span className="text-overline text-muted-foreground/60 uppercase tracking-widest">
            {section.label}
          </span>
        </div>
      )}
      {!isOpen && <div className="mb-1 mx-3 h-px bg-border/60" />}
      <div className="space-y-0.5 px-2">
        {section.items.map(renderNavItem)}
      </div>
    </div>
  );

  return (
    <motion.aside
      id="app-sidebar"
      initial={false}
      animate={{ width: isOpen ? OPEN_WIDTH : COLLAPSED_WIDTH }}
      transition={{ duration: TRANSITION_DURATION, ease: [0.4, 0, 0.2, 1] }}
      className={cn(
        'flex flex-col h-screen shrink-0 overflow-hidden z-20 relative',
        'border-r border-border bg-sidebar',
        'selection:bg-primary/20 selection:text-primary',
      )}
    >
      {/* ── Brand ── */}
      <div
        className="h-14 flex items-center px-4 border-b border-border shrink-0 cursor-pointer gap-2.5"
        onClick={() => navigate(ROUTES.DASHBOARD)}
        role="button"
        tabIndex={0}
        aria-label="Go to dashboard"
        onKeyDown={(e) => e.key === 'Enter' && navigate(ROUTES.DASHBOARD)}
      >
        <ShieldCheck className="h-5 w-5 text-primary shrink-0" aria-hidden="true" />
        <AnimatePresence>
          {isOpen && (
            <motion.div
              key="brand-text"
              initial={{ opacity: 0, x: -8 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -8 }}
              transition={{ duration: 0.15 }}
              className="overflow-hidden"
            >
              <span className="text-heading-sm font-semibold whitespace-nowrap tracking-tight">
                FairTrace
              </span>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* ── Navigation ── */}
      <nav
        className="flex-1 overflow-y-auto py-4 scrollbar-hide"
        aria-label="Main navigation"
      >
        {navSections.map(renderSection)}
      </nav>

      {/* ── User Footer ── */}
      <div className="border-t border-border shrink-0">
        {/* User profile row */}
        <div
          className={cn(
            'flex items-center gap-2.5 px-3 py-3 mx-2 mt-2 mb-1 rounded-md',
            'cursor-pointer transition-colors duration-[120ms]',
            'hover:bg-muted/60 group',
          )}
          title={!isOpen ? (user?.full_name ?? 'Profile') : undefined}
          role="button"
          tabIndex={0}
          aria-label="User profile"
        >
          {/* Avatar */}
          <div className="h-7 w-7 rounded-full bg-primary/15 border border-primary/25 flex items-center justify-center text-primary text-[10px] font-semibold shrink-0 select-none">
            {initials}
          </div>
          <AnimatePresence>
            {isOpen && (
              <motion.div
                initial={{ opacity: 0, x: -4 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.12 }}
                className="flex-1 min-w-0 overflow-hidden"
              >
                <p className="text-body font-medium text-foreground truncate leading-tight">
                  {user?.full_name ?? 'User'}
                </p>
                <p className="text-label text-muted-foreground truncate leading-tight">
                  {roleLabel}
                </p>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Logout */}
        <div className="px-2 pb-2">
          <button
            onClick={handleLogout}
            title={!isOpen ? 'Sign out' : undefined}
            className={cn(
              'flex w-full items-center gap-2.5 px-3 py-2 rounded-md',
              'text-body text-muted-foreground',
              'transition-colors duration-[120ms]',
              'hover:bg-danger/8 hover:text-danger',
              'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring/50',
            )}
            aria-label="Sign out"
          >
            <LogOut className="h-4 w-4 shrink-0" aria-hidden="true" />
            <AnimatePresence>
              {isOpen && (
                <motion.span
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  transition={{ duration: 0.1 }}
                  className="text-body"
                >
                  Sign out
                </motion.span>
              )}
            </AnimatePresence>
          </button>
        </div>

        {/* ── Collapse toggle ── */}
        <div className="border-t border-border p-2">
          <button
            id="sidebar-collapse-btn"
            onClick={() => setIsOpen(!isOpen)}
            className={cn(
              'flex w-full items-center rounded-md px-3 py-2',
              'text-muted-foreground transition-colors duration-[120ms]',
              'hover:bg-muted/60 hover:text-foreground',
              'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring/50',
              isOpen ? 'justify-between' : 'justify-center',
            )}
            aria-label={isOpen ? 'Collapse sidebar (⌘B)' : 'Expand sidebar (⌘B)'}
            title="Toggle Sidebar (⌘B)"
          >
            {isOpen ? (
              <>
                <span className="text-label text-muted-foreground/60">⌘B</span>
                <ChevronsLeft className="h-4 w-4" aria-hidden="true" />
              </>
            ) : (
              <ChevronsRight className="h-4 w-4" aria-hidden="true" />
            )}
          </button>
        </div>
      </div>
    </motion.aside>
  );
}
