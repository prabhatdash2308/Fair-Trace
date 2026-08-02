import * as React from 'react';
import { Command } from 'cmdk';
import { Search, FileText, Users, Activity, ArrowRight, LayoutDashboard, Settings } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { cn } from '@/lib/utils';
import { ROUTES } from '@/constants/routes';

interface SearchItem {
  id: string;
  label: string;
  description?: string;
  icon: React.ElementType;
  action: () => void;
  group: string;
  kbd?: string;
}

/**
 * GlobalSearch — Linear-style command palette.
 * ⌘K to open. ESC to close.
 * Keyboard navigation: ↑↓ to move, Enter to select.
 * Footer: keyboard shortcut hints.
 */
export function GlobalSearch() {
  const [open, setOpen] = React.useState(false);
  const [query, setQuery] = React.useState('');
  const navigate = useNavigate();

  React.useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setOpen((o) => !o);
      }
      if (e.key === 'Escape' && open) {
        setOpen(false);
      }
    };
    document.addEventListener('keydown', down);
    return () => document.removeEventListener('keydown', down);
  }, [open]);

  const runCommand = React.useCallback((action: () => void) => {
    setOpen(false);
    setQuery('');
    action();
  }, []);

  const items: SearchItem[] = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      description: 'Executive overview and metrics',
      icon: LayoutDashboard,
      action: () => navigate(ROUTES.DASHBOARD),
      group: 'Navigation',
    },
    {
      id: 'employees',
      label: 'Employee Directory',
      description: 'Browse and manage workforce',
      icon: Users,
      action: () => navigate(ROUTES.EMPLOYEES),
      group: 'Navigation',
    },


    {
      id: 'settings',
      label: 'Settings',
      description: 'Configure workspace and AI',
      icon: Settings,
      action: () => navigate(ROUTES.SETTINGS),
      group: 'System',
    },
  ];

  const filtered = query
    ? items.filter(
        (item) =>
          item.label.toLowerCase().includes(query.toLowerCase()) ||
          item.description?.toLowerCase().includes(query.toLowerCase())
      )
    : items;

  const groups = Array.from(new Set(filtered.map((i) => i.group)));

  return (
    <>
      {/* ── Trigger button ── */}
      <button
        onClick={() => setOpen(true)}
        className={cn(
          'hidden md:flex items-center justify-between gap-2',
          'h-8 w-56 px-3 rounded-md',
          'bg-muted/50 border border-border/60',
          'text-caption text-muted-foreground',
          'hover:bg-muted hover:border-border',
          'transition-colors duration-[120ms]',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring/50',
        )}
        aria-label="Open command palette (⌘K)"
      >
        <div className="flex items-center gap-1.5">
          <Search className="h-3.5 w-3.5" aria-hidden="true" />
          <span>Search…</span>
        </div>
        <kbd className={cn(
          'inline-flex items-center gap-0.5 px-1.5 py-0.5',
          'rounded border border-border/60 bg-background/80',
          'font-mono text-[10px] text-muted-foreground',
          'pointer-events-none select-none',
        )}>
          <span>⌘</span>K
        </kbd>
      </button>

      {/* ── Command Palette Dialog ── */}
      <AnimatePresence>
        {open && (
          <div className="fixed inset-0 z-50 flex items-start justify-center pt-[15vh] px-4">
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.15 }}
              className="fixed inset-0 bg-background/70 backdrop-blur-sm"
              onClick={() => setOpen(false)}
              aria-hidden="true"
            />

            {/* Dialog */}
            <motion.div
              initial={{ opacity: 0, scale: 0.97, y: -12 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.97, y: -8 }}
              transition={{ duration: 0.18, ease: [0.16, 1, 0.3, 1] }}
              className={cn(
                'relative w-full max-w-[560px]',
                'rounded-xl border border-border bg-popover',
                'shadow-floating overflow-hidden',
              )}
              role="dialog"
              aria-modal="true"
              aria-label="Command palette"
            >
              <Command
                className="flex flex-col w-full bg-transparent"
                shouldFilter={false}
              >
                {/* Search input */}
                <div className="flex items-center gap-3 px-4 py-3 border-b border-border">
                  <Search className="h-4 w-4 text-muted-foreground shrink-0" aria-hidden="true" />
                  <Command.Input
                    autoFocus
                    placeholder="Search pages, employees, reports…"
                    value={query}
                    onValueChange={setQuery}
                    className={cn(
                      'flex-1 bg-transparent outline-none',
                      'text-body text-foreground placeholder:text-muted-foreground/60',
                    )}
                    aria-label="Search"
                  />
                  <kbd className={cn(
                    'inline-flex items-center px-1.5 py-0.5 rounded',
                    'border border-border bg-muted',
                    'font-mono text-[10px] text-muted-foreground',
                    'pointer-events-none select-none',
                  )}>
                    ESC
                  </kbd>
                </div>

                {/* Results */}
                <Command.List
                  className="max-h-[320px] overflow-y-auto py-2 scrollbar-thin"
                  aria-label="Search results"
                >
                  <Command.Empty className="py-10 text-center text-body text-muted-foreground">
                    No results for <span className="font-medium text-foreground">"{query}"</span>
                  </Command.Empty>

                  {groups.map((group) => (
                    <Command.Group
                      key={group}
                      heading={group}
                      className="px-2 py-1 [&>[cmdk-group-heading]]:text-overline [&>[cmdk-group-heading]]:text-muted-foreground [&>[cmdk-group-heading]]:px-2 [&>[cmdk-group-heading]]:py-1.5 [&>[cmdk-group-heading]]:uppercase [&>[cmdk-group-heading]]:tracking-widest"
                    >
                      {filtered
                        .filter((item) => item.group === group)
                        .map((item) => (
                          <Command.Item
                            key={item.id}
                            value={item.id}
                            onSelect={() => runCommand(item.action)}
                            className={cn(
                              'flex items-center gap-3 px-2 py-2 rounded-md mx-0.5',
                              'text-body text-foreground cursor-pointer',
                              'transition-colors duration-[80ms]',
                              'hover:bg-muted aria-selected:bg-muted',
                              'focus:outline-none',
                            )}
                          >
                            <div className="flex items-center justify-center h-7 w-7 rounded-md bg-muted/80 border border-border/60 shrink-0">
                              <item.icon className="h-3.5 w-3.5 text-muted-foreground" aria-hidden="true" />
                            </div>
                            <div className="flex-1 min-w-0">
                              <p className="text-body font-medium text-foreground">{item.label}</p>
                              {item.description && (
                                <p className="text-caption text-muted-foreground truncate">{item.description}</p>
                              )}
                            </div>
                            <ArrowRight className="h-3.5 w-3.5 text-muted-foreground/50 shrink-0" aria-hidden="true" />
                          </Command.Item>
                        ))}
                    </Command.Group>
                  ))}
                </Command.List>

                {/* ── Footer — keyboard shortcut hints ── */}
                <div className="border-t border-border px-3 py-2 flex items-center justify-between">
                  <div className="flex items-center gap-3 text-[10px] text-muted-foreground/60">
                    <span className="flex items-center gap-1">
                      <kbd className="inline-flex items-center px-1 py-0.5 rounded border border-border bg-muted font-mono text-[9px]">↑↓</kbd>
                      Navigate
                    </span>
                    <span className="flex items-center gap-1">
                      <kbd className="inline-flex items-center px-1 py-0.5 rounded border border-border bg-muted font-mono text-[9px]">↵</kbd>
                      Select
                    </span>
                    <span className="flex items-center gap-1">
                      <kbd className="inline-flex items-center px-1 py-0.5 rounded border border-border bg-muted font-mono text-[9px]">ESC</kbd>
                      Close
                    </span>
                  </div>
                  <span className="text-[10px] text-muted-foreground/40 font-medium">
                    ReviewGuard AI
                  </span>
                </div>
              </Command>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </>
  );
}
