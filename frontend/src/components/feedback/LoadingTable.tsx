import * as React from 'react';
import { Loader2 } from 'lucide-react';

export const LoadingTable: React.FC<{ rows?: number }> = ({ rows = 5 }) => {
  return (
    <div className="w-full animate-pulse rounded-md border">
      <div className="h-10 border-b bg-muted/50" />
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="flex h-14 items-center justify-between border-b px-4">
          <div className="h-4 w-1/4 rounded bg-muted" />
          <div className="h-4 w-1/4 rounded bg-muted" />
          <div className="h-4 w-1/4 rounded bg-muted" />
          <div className="h-8 w-8 rounded-full bg-muted" />
        </div>
      ))}
      <div className="flex items-center justify-center py-4">
        <Loader2 className="h-5 w-5 animate-spin text-muted-foreground" />
      </div>
    </div>
  );
};
