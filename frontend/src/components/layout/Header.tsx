import { Bell, Search, Menu, Moon, Sun } from "lucide-react";
import { useEffect, useState } from "react";

interface HeaderProps {
  sidebarOpen: boolean;
  setSidebarOpen: (isOpen: boolean) => void;
}

export function Header({ sidebarOpen, setSidebarOpen }: HeaderProps) {
  const [isDark, setIsDark] = useState(true);

  useEffect(() => {
    // Initial load
    if (document.documentElement.classList.contains('dark')) {
      setIsDark(true);
    } else {
      // Default to dark
      document.documentElement.classList.add('dark');
      setIsDark(true);
    }
  }, []);

  const toggleTheme = () => {
    if (isDark) {
      document.documentElement.classList.remove('dark');
      setIsDark(false);
    } else {
      document.documentElement.classList.add('dark');
      setIsDark(true);
    }
  };

  return (
    <header className="h-16 border-b border-border bg-card flex items-center justify-between px-6 z-10 shrink-0">
      <div className="flex items-center flex-1">
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="mr-4 lg:hidden text-muted-foreground hover:text-foreground"
        >
          <Menu className="h-5 w-5" />
        </button>
        <div className="max-w-md w-full relative hidden sm:block">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search employees, reviews, or insights..."
            className="w-full pl-9 pr-4 py-2 bg-background border border-border rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-brand-blue/50 transition-all placeholder:text-muted-foreground"
          />
        </div>
      </div>
      
      <div className="flex items-center space-x-4">
        <button 
          onClick={toggleTheme}
          className="p-2 text-muted-foreground hover:bg-muted rounded-full transition-colors"
        >
          {isDark ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
        </button>
        <button className="p-2 text-muted-foreground hover:bg-muted rounded-full transition-colors relative">
          <Bell className="h-5 w-5" />
          <span className="absolute top-2 right-2 h-2 w-2 bg-danger-red rounded-full ring-2 ring-card"></span>
        </button>
        <div className="h-8 w-8 rounded-full bg-brand-blue flex items-center justify-center text-primary-foreground font-semibold text-sm">
          JD
        </div>
      </div>
    </header>
  );
}
