import { Bell, Menu, Moon, Sun, Building, ChevronDown } from 'lucide-react';
import { useTheme } from '@/hooks/useTheme';
import { useAuthStore } from '@/store';
import { GlobalSearch } from './GlobalSearch';
import { Breadcrumbs } from './Breadcrumbs';
import { cn } from '@/lib/utils';
import { ROLE_LABELS } from '@/constants/roles';

interface HeaderProps {
  sidebarOpen: boolean;
  setSidebarOpen: (isOpen: boolean) => void;
}

/**
 * Header — top navigation bar.
 * Sticky, 56px (h-14), minimal visual noise.
 * Search centered, actions on right, breadcrumb on left.
 */
export function Header({ sidebarOpen, setSidebarOpen }: HeaderProps) {
  const { resolvedTheme, toggleTheme } = useTheme();
  const { user } = useAuthStore();

  const initials = user?.full_name
    ? user.full_name.split(' ').map((n) => n[0]).slice(0, 2).join('').toUpperCase()
    : 'RG';

  const roleLabel = user?.role ? ROLE_LABELS[user.role as keyof typeof ROLE_LABELS] : '';

  return (
    <header
      className={cn(
        'h-14 border-b border-border bg-card',
        'flex items-center justify-between px-4',
        'sticky top-0 z-30 shrink-0',
      )}
    >
      {/* ── Left: Menu toggle + Breadcrumbs ── */}
      <div className="flex items-center gap-3 flex-1 min-w-0">
        <button
          id="sidebar-toggle"
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className={cn(
            'flex items-center justify-center h-8 w-8 rounded-md shrink-0',
            'text-muted-foreground hover:text-foreground hover:bg-muted/70',
            'transition-colors duration-[120ms]',
            'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring/50',
          )}
          aria-label="Toggle sidebar"
        >
          <Menu className="h-4 w-4" aria-hidden="true" />
        </button>

        <div className="h-4 w-px bg-border/70 shrink-0" />

        <div className="hidden sm:flex items-center min-w-0">
          <Breadcrumbs />
        </div>
      </div>

      {/* ── Center: Global Search ── */}
      <div className="flex-shrink-0 flex justify-center px-4">
        <GlobalSearch />
      </div>

      {/* ── Right: Actions + Avatar ── */}
      <div className="flex items-center gap-1 flex-1 justify-end">

        {/* Workspace switcher */}
        <button
          className={cn(
            'hidden md:flex items-center gap-1.5 h-8 px-2.5 rounded-md shrink-0',
            'text-muted-foreground hover:text-foreground hover:bg-muted/70',
            'transition-colors duration-[120ms] max-w-[130px]',
            'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring/50',
          )}
          aria-label="Switch workspace"
        >
          <Building className="h-3.5 w-3.5 shrink-0" aria-hidden="true" />
          <span className="text-caption font-medium truncate">Acme Corp</span>
          <ChevronDown className="h-3 w-3 shrink-0 opacity-60" aria-hidden="true" />
        </button>

        <div className="h-4 w-px bg-border/70 mx-0.5 hidden md:block shrink-0" />

        {/* Theme toggle */}
        <button
          id="theme-toggle"
          onClick={toggleTheme}
          className={cn(
            'flex items-center justify-center h-8 w-8 rounded-md',
            'text-muted-foreground hover:text-foreground hover:bg-muted/70',
            'transition-colors duration-[120ms]',
            'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring/50',
          )}
          aria-label={resolvedTheme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
        >
          {resolvedTheme === 'dark'
            ? <Sun className="h-4 w-4" aria-hidden="true" />
            : <Moon className="h-4 w-4" aria-hidden="true" />
          }
        </button>

        {/* Notifications */}
        <button
          id="notifications-btn"
          className={cn(
            'relative flex items-center justify-center h-8 w-8 rounded-md',
            'text-muted-foreground hover:text-foreground hover:bg-muted/70',
            'transition-colors duration-[120ms]',
            'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring/50',
          )}
          aria-label="Notifications (1 unread)"
        >
          <Bell className="h-4 w-4" aria-hidden="true" />
          <span
            className="absolute top-1.5 right-1.5 h-1.5 w-1.5 bg-danger rounded-full"
            aria-hidden="true"
          />
        </button>

        <div className="h-4 w-px bg-border/70 mx-1 shrink-0" />

        {/* User avatar */}
        <button
          id="user-avatar"
          className={cn(
            'flex items-center gap-2 h-8 rounded-md px-1.5',
            'hover:bg-muted/70 transition-colors duration-[120ms]',
            'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring/50',
          )}
          aria-label={`${user?.full_name ?? 'User'} — ${roleLabel}`}
          title={`${user?.full_name ?? 'User'}\n${roleLabel}`}
        >
          <div className={cn(
            'h-7 w-7 rounded-full shrink-0',
            'bg-primary/15 border border-primary/25',
            'flex items-center justify-center',
            'text-primary font-semibold text-[10px]',
            'select-none',
          )}>
            {initials}
          </div>
          <span className="hidden lg:block text-caption font-medium text-foreground max-w-[80px] truncate">
            {user?.full_name?.split(' ')[0] ?? 'User'}
          </span>
        </button>
      </div>
    </header>
  );
}
