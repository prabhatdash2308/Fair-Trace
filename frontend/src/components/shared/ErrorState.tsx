import { motion } from 'framer-motion';
import { AlertTriangle, RefreshCw, Home } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';

interface ErrorStateProps {
  title?: string;
  message?: string;
  onRetry?: () => void;
  onHome?: () => void;
  className?: string;
}

/**
 * ErrorState — premium error display with retry and home actions.
 * Uses semantic error colors, Framer Motion entrance, Button component.
 */
export function ErrorState({
  title = 'Something went wrong',
  message = 'An unexpected error occurred. Please try again or return to the dashboard.',
  onRetry,
  onHome,
  className,
}: ErrorStateProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
      className={cn(
        'flex flex-col items-center justify-center text-center py-16 px-6',
        className
      )}
      role="alert"
      aria-live="assertive"
    >
      <div className="p-3 rounded-xl bg-danger/8 border border-danger/20 mb-4">
        <AlertTriangle className="h-6 w-6 text-danger" aria-hidden="true" />
      </div>

      <h3 className="text-heading-md font-semibold text-foreground mb-1.5">{title}</h3>
      <p className="text-body text-muted-foreground max-w-sm leading-relaxed mb-6">{message}</p>

      <div className="flex items-center gap-3">
        {onRetry && (
          <Button
            id="error-retry-btn"
            variant="outline"
            size="sm"
            onClick={onRetry}
          >
            <RefreshCw className="h-4 w-4" />
            Try again
          </Button>
        )}
        {onHome && (
          <Button
            id="error-home-btn"
            variant="ghost"
            size="sm"
            onClick={onHome}
          >
            <Home className="h-4 w-4" />
            Dashboard
          </Button>
        )}
      </div>
    </motion.div>
  );
}
