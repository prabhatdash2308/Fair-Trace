import { cn } from '@/lib/utils';

interface LoadingStateProps {
  text?: string;
  rows?: number;
  variant?: 'default' | 'card' | 'table' | 'metric';
  className?: string;
}

/**
 * LoadingState — shimmer skeleton placeholder.
 * Uses animate-shimmer for premium loading feel (not just opacity pulse).
 * Supports different layouts: default (rows), card, table, metric.
 */
export function LoadingState({ text, rows = 3, variant = 'default', className }: LoadingStateProps) {
  return (
    <div
      className={cn('', className)}
      aria-live="polite"
      aria-label={text ?? 'Loading…'}
      aria-busy="true"
    >
      {text && (
        <p className="text-caption text-muted-foreground mb-3 animate-pulse">{text}</p>
      )}

      {variant === 'default' && (
        <div className="space-y-3">
          {Array.from({ length: rows }).map((_, i) => (
            <div key={i} className="space-y-1.5">
              <div
                className="h-4 rounded-md animate-shimmer"
                style={{ width: `${85 - i * 8}%` }}
              />
              <div className="h-3 rounded-md animate-shimmer w-3/5" />
            </div>
          ))}
        </div>
      )}

      {variant === 'card' && (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {Array.from({ length: rows }).map((_, i) => (
            <div key={i} className="rounded-lg border border-border bg-card p-6 space-y-3">
              <div className="h-3 w-20 rounded-md animate-shimmer" />
              <div className="h-8 w-14 rounded-md animate-shimmer" />
              <div className="h-2.5 w-28 rounded-md animate-shimmer" />
            </div>
          ))}
        </div>
      )}

      {variant === 'table' && (
        <div className="rounded-lg border border-border overflow-hidden bg-card">
          {/* Header */}
          <div className="flex gap-4 px-3 py-2.5 border-b border-border bg-muted/30">
            {[40, 25, 15, 10].map((w, i) => (
              <div key={i} className="h-3 rounded-md animate-shimmer" style={{ width: `${w}%` }} />
            ))}
          </div>
          {/* Rows */}
          {Array.from({ length: rows }).map((_, i) => (
            <div
              key={i}
              className="flex gap-4 px-3 py-3 border-b border-border/60 last:border-0"
            >
              <div className="flex items-center gap-2.5" style={{ width: '40%' }}>
                <div className="h-8 w-8 rounded-full animate-shimmer shrink-0" />
                <div className="flex-1 space-y-1">
                  <div className="h-3.5 rounded-md animate-shimmer w-full" />
                  <div className="h-2.5 rounded-md animate-shimmer w-2/3" />
                </div>
              </div>
              {[25, 15, 10].map((w, j) => (
                <div key={j} className="flex items-center" style={{ width: `${w}%` }}>
                  <div className="h-3 rounded-md animate-shimmer w-full" />
                </div>
              ))}
            </div>
          ))}
        </div>
      )}

      {variant === 'metric' && (
        <div className="rounded-lg border border-border bg-card p-6 space-y-4">
          <div className="flex items-center justify-between">
            <div className="h-3 w-24 rounded-md animate-shimmer" />
            <div className="h-8 w-8 rounded-lg animate-shimmer" />
          </div>
          <div className="h-9 w-20 rounded-md animate-shimmer" />
          <div className="h-2.5 w-32 rounded-md animate-shimmer" />
        </div>
      )}
    </div>
  );
}
