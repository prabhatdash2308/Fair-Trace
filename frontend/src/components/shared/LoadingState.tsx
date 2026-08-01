import { cn } from '@/lib/utils';
import type { LoadingStateProps } from '@/types/ui.types';

/**
 * LoadingState — skeleton placeholder for async content.
 * Renders configurable rows of pulsing skeleton blocks.
 */
export function LoadingState({ text, rows = 3, className }: LoadingStateProps) {
  return (
    <div className={cn('space-y-4', className)} aria-live="polite" aria-label={text ?? 'Loading…'}>
      {text && (
        <p className="text-sm text-muted-foreground animate-pulse">{text}</p>
      )}
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="space-y-2 animate-pulse">
          <div
            className="h-4 bg-muted rounded"
            style={{ width: `${90 - i * 10}%` }}
          />
          <div className="h-3 bg-muted rounded w-3/4" />
        </div>
      ))}
    </div>
  );
}
