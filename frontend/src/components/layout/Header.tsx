import { Bell, Menu, Moon, Sun, Building } from 'lucide-react';
import { useTheme } from '@/hooks/useTheme';
import { useAuthStore } from '@/store';
import { GlobalSearch } from './GlobalSearch';
import { Breadcrumbs } from './Breadcrumbs';

interface HeaderProps {
  sidebarOpen: boolean;
  setSidebarOpen: (isOpen: boolean) => void;
}

export function Header({ sidebarOpen, setSidebarOpen }: HeaderProps) {
  const { resolvedTheme, toggleTheme } = useTheme();
  const { user } = useAuthStore();

  const initials = user?.full_name
    ? user.full_name.split(' ').map((n) => n[0]).slice(0, 2).join('').toUpperCase()
    : 'RG';

  return (
    <header className="h-14 border-b border-border bg-card flex items-center justify-between px-4 z-10 shrink-0">
      {/* Left: Menu toggle + Breadcrumbs */}
      <div className="flex items-center gap-3 flex-1 min-w-0">
        <button
          id="sidebar-toggle"
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="text-muted-foreground hover:text-foreground transition-colors shrink-0"
          aria-label="Toggle sidebar"
        >
          <Menu className="h-4 w-4" />
        </button>
        
        <div className="h-4 w-px bg-border mx-1 shrink-0" />

        <div className="hidden sm:flex items-center gap-2 truncate">
          <Breadcrumbs />
        </div>
      </div>

      {/* Center: Search (Command Palette) */}
      <div className="flex-1 flex justify-center max-w-md px-4">
        <GlobalSearch />
      </div>

      {/* Right: Theme + Notifications + Workspace + Avatar */}
      <div className="flex items-center gap-1.5 flex-1 justify-end">
        
        <button
          onClick={() => {}}
          className="hidden md:flex items-center gap-2 px-2 py-1.5 text-sm text-muted-foreground hover:bg-muted hover:text-foreground rounded-md transition-colors"
        >
          <Building className="h-4 w-4" />
          <span className="font-medium truncate max-w-[100px]">Acme Corp</span>
        </button>

        <div className="h-4 w-px bg-border mx-1 hidden md:block shrink-0" />

        <button
          id="theme-toggle"
          onClick={toggleTheme}
          className="p-1.5 text-muted-foreground hover:text-foreground hover:bg-muted rounded-md transition-colors"
          aria-label="Toggle theme"
        >
          {resolvedTheme === 'dark' ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
        </button>

        <button
          id="notifications-btn"
          className="p-1.5 text-muted-foreground hover:text-foreground hover:bg-muted rounded-md transition-colors relative"
          aria-label="Notifications"
        >
          <Bell className="h-4 w-4" />
          <span className="absolute top-1 right-1 h-1.5 w-1.5 bg-destructive rounded-full" />
        </button>

        <div
          id="user-avatar"
          className="h-7 w-7 rounded-full bg-primary/20 border border-primary/30 flex items-center justify-center text-primary font-semibold text-xs select-none cursor-pointer ml-2 shrink-0"
          title={user?.full_name ?? 'User'}
        >
          {initials}
        </div>
      </div>
    </header>
  );
}
