import { AlertTriangle, RefreshCw } from 'lucide-react';
import { cn } from '@/lib/utils';
import type { ErrorStateProps } from '@/types/ui.types';

/**
 * ErrorState — shown when a query or action fails.
 * Provides a retry action and displays a user-friendly error message.
 */
export function ErrorState({
  title = 'Something went wrong',
  message = 'An unexpected error occurred. Please try again.',
  onRetry,
  className,
}: ErrorStateProps) {
  return (
    <div
      className={cn(
        'flex flex-col items-center justify-center text-center py-16 px-6',
        className
      )}
      role="alert"
      aria-live="assertive"
    >
      <div className="p-4 rounded-full bg-destructive/10 mb-4">
        <AlertTriangle className="h-8 w-8 text-destructive" aria-hidden="true" />
      </div>

      <h3 className="text-base font-semibold text-foreground mb-1">{title}</h3>
      <p className="text-sm text-muted-foreground max-w-sm">{message}</p>

      {onRetry && (
        <button
          id="error-retry-btn"
          onClick={onRetry}
          className="mt-6 flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-md border border-border bg-card text-foreground hover:bg-muted transition-colors"
        >
          <RefreshCw className="h-4 w-4" />
          Try again
        </button>
      )}
    </div>
  );
}
