import * as React from 'react';
import { cn } from '@/lib/utils';
import { ScrollArea } from '@/components/ui/scroll-area';

export interface LogViewerProps {
  logs: string;
  className?: string;
}

export const LogViewer: React.FC<LogViewerProps> = ({ logs, className }) => {
  if (!logs) {
    return (
      <div className={cn("flex h-32 items-center justify-center rounded-md border border-border/50 bg-muted/20 text-sm text-muted-foreground", className)}>
        No logs available for this node.
      </div>
    );
  }

  return (
    <div className={cn("rounded-md border border-border/50 bg-[#0d1117] overflow-hidden", className)}>
      <div className="flex items-center px-4 py-2 border-b border-border/10 bg-[#161b22]">
        <span className="text-xs font-mono text-muted-foreground">Execution Logs</span>
      </div>
      <ScrollArea className="h-64 w-full">
        <pre className="p-4 text-xs font-mono text-[#e6edf3] whitespace-pre-wrap break-words">
          {logs}
        </pre>
      </ScrollArea>
    </div>
  );
};
