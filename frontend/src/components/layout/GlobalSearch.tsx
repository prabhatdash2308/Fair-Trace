import * as React from 'react';
import { Command } from 'cmdk';
import { Search, FileText, Users, Activity, Loader2, ArrowRight } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { ROUTES } from '@/constants/routes';

export function GlobalSearch() {
  const [open, setOpen] = React.useState(false);
  const [query, setQuery] = React.useState('');
  const navigate = useNavigate();

  React.useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setOpen((open) => !open);
      }
    };
    document.addEventListener('keydown', down);
    return () => document.removeEventListener('keydown', down);
  }, []);

  const runCommand = React.useCallback((command: () => void) => {
    setOpen(false);
    command();
  }, []);

  return (
    <>
      <button
        onClick={() => setOpen(true)}
        className="hidden md:flex items-center gap-2 px-3 py-1.5 bg-muted/50 hover:bg-muted text-muted-foreground border border-border/50 rounded-md text-sm transition-colors w-64 justify-between group"
      >
        <div className="flex items-center gap-2">
          <Search className="h-4 w-4" />
          <span>Search workspace...</span>
        </div>
        <kbd className="pointer-events-none inline-flex h-5 select-none items-center gap-1 rounded border border-border bg-muted px-1.5 font-mono text-[10px] font-medium opacity-100 group-hover:bg-background">
          <span className="text-xs">⌘</span>K
        </kbd>
      </button>

      <AnimatePresence>
        {open && (
          <div className="fixed inset-0 z-50 flex items-start justify-center pt-[15vh] sm:pt-[20vh] px-4">
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-background/80 backdrop-blur-sm"
              onClick={() => setOpen(false)}
            />
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: -20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: -20 }}
              transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
              className="relative w-full max-w-lg bg-card border border-border shadow-2xl rounded-xl overflow-hidden"
            >
              <Command className="flex flex-col w-full h-full bg-transparent" shouldFilter={false}>
                <div className="flex items-center border-b border-border px-4 py-3">
                  <Search className="h-5 w-5 text-muted-foreground shrink-0 mr-3" />
                  <Command.Input
                    autoFocus
                    placeholder="Search employees, reports, and pipelines..."
                    value={query}
                    onValueChange={setQuery}
                    className="flex-1 bg-transparent outline-none text-base placeholder:text-muted-foreground text-foreground"
                  />
                  <kbd className="pointer-events-none inline-flex h-5 select-none items-center gap-1 rounded border border-border bg-muted px-1.5 font-mono text-[10px] font-medium text-muted-foreground">
                    ESC
                  </kbd>
                </div>

                <Command.List className="max-h-[300px] overflow-y-auto p-2 scrollbar-thin scrollbar-thumb-border scrollbar-track-transparent">
                  <Command.Empty className="py-6 text-center text-sm text-muted-foreground">
                    No results found. (Mock search only)
                  </Command.Empty>

                  <Command.Group heading="Suggestions" className="px-2 py-1 text-xs font-medium text-muted-foreground">
                    <Command.Item 
                      onSelect={() => runCommand(() => navigate(ROUTES.EMPLOYEES))}
                      className="flex items-center px-2 py-2 mt-1 rounded-md text-sm text-foreground cursor-pointer hover:bg-muted aria-selected:bg-muted transition-colors"
                    >
                      <Users className="h-4 w-4 mr-2 text-muted-foreground" />
                      View all employees
                    </Command.Item>
                    <Command.Item 
                      onSelect={() => runCommand(() => navigate(ROUTES.REPORTS))}
                      className="flex items-center px-2 py-2 mt-1 rounded-md text-sm text-foreground cursor-pointer hover:bg-muted aria-selected:bg-muted transition-colors"
                    >
                      <FileText className="h-4 w-4 mr-2 text-muted-foreground" />
                      View recent AI reports
                    </Command.Item>
                    <Command.Item 
                      onSelect={() => runCommand(() => navigate(ROUTES.PIPELINE))}
                      className="flex items-center px-2 py-2 mt-1 rounded-md text-sm text-foreground cursor-pointer hover:bg-muted aria-selected:bg-muted transition-colors"
                    >
                      <Activity className="h-4 w-4 mr-2 text-muted-foreground" />
                      Monitor AI Pipeline Status
                    </Command.Item>
                  </Command.Group>
                </Command.List>
              </Command>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </>
  );
}
