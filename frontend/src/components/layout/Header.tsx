import { Bell, Search, Menu, Moon, Sun } from 'lucide-react';
import { useTheme } from '@/hooks/useTheme';
import { useAuthStore } from '@/store';

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
    <header className="h-16 border-b border-border bg-card flex items-center justify-between px-6 z-10 shrink-0">
      {/* Left: Menu toggle + Search */}
      <div className="flex items-center flex-1 gap-4">
        <button
          id="sidebar-toggle"
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="text-muted-foreground hover:text-foreground transition-colors"
          aria-label="Toggle sidebar"
        >
          <Menu className="h-5 w-5" />
        </button>

        <div className="max-w-md w-full relative hidden sm:block">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />
          <input
            id="global-search"
            type="text"
            placeholder="Search employees, reviews, or insights..."
            className="w-full pl-9 pr-4 py-2 bg-background border border-border rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-primary/40 transition-all placeholder:text-muted-foreground"
          />
        </div>
      </div>

      {/* Right: Theme + Notifications + Avatar */}
      <div className="flex items-center gap-2">
        <button
          id="theme-toggle"
          onClick={toggleTheme}
          className="p-2 text-muted-foreground hover:text-foreground hover:bg-muted rounded-full transition-colors"
          aria-label="Toggle theme"
        >
          {resolvedTheme === 'dark' ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
        </button>

        <button
          id="notifications-btn"
          className="p-2 text-muted-foreground hover:text-foreground hover:bg-muted rounded-full transition-colors relative"
          aria-label="Notifications"
        >
          <Bell className="h-5 w-5" />
          <span className="absolute top-2 right-2 h-2 w-2 bg-destructive rounded-full ring-2 ring-card" />
        </button>

        <div
          id="user-avatar"
          className="h-8 w-8 rounded-full bg-primary flex items-center justify-center text-primary-foreground font-semibold text-sm select-none cursor-pointer"
          title={user?.full_name ?? 'User'}
        >
          {initials}
        </div>
      </div>
    </header>
  );
}
