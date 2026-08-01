import * as React from 'react';
import { cn } from '@/lib/utils';
import type { UINode } from '@/features/pipeline/utils';

export interface ExecutionNodeProps {
  node: UINode;
  isLast?: boolean;
  onClick?: (node: UINode) => void;
  isActive?: boolean;
}

export const ExecutionNode: React.FC<ExecutionNodeProps> = ({ node, isLast, onClick, isActive }) => {
  const Icon = node.statusConfig.icon;
  const isPending = node.normalizedStatus === 'PENDING';
  
  return (
    <div 
      className={cn(
        "relative flex items-center p-3 rounded-lg border transition-all cursor-pointer group",
        isActive ? "border-primary bg-primary/5 shadow-sm" : "border-border/50 hover:border-border hover:bg-muted/30",
        isPending && "opacity-70"
      )}
      onClick={() => onClick?.(node)}
    >
      <div className={cn("flex h-8 w-8 shrink-0 items-center justify-center rounded-md mr-3", node.statusConfig.bg)}>
        <Icon className={cn("h-4 w-4", node.statusConfig.color, node.statusConfig.animation)} />
      </div>
      
      <div className="flex flex-col min-w-0">
        <span className={cn("text-sm font-medium truncate", isActive ? "text-foreground" : "text-muted-foreground group-hover:text-foreground")}>
          {node.title}
        </span>
        <span className="text-xs text-muted-foreground truncate">
          {node.latencyMs ? `${node.latencyMs}ms` : node.statusLabel}
        </span>
      </div>

      {!isLast && (
        <div className="absolute top-full left-7 -ml-px h-4 w-px bg-border/50 z-0 hidden md:block" />
      )}
    </div>
  );
};
