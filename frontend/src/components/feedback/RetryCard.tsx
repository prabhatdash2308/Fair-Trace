import * as React from 'react';
import { AlertCircle, RefreshCw } from 'lucide-react';
import { PrimaryButton } from '@/components/ui/PrimaryButton';

interface RetryCardProps {
  error: string;
  onRetry: () => void;
}

export const RetryCard: React.FC<RetryCardProps> = ({ error, onRetry }) => {
  return (
    <div className="flex flex-col items-center justify-center rounded-lg border border-destructive/20 bg-destructive/5 p-8 text-center">
      <AlertCircle className="mb-4 h-10 w-10 text-destructive" />
      <h3 className="mb-2 text-lg font-medium text-foreground">Failed to load data</h3>
      <p className="mb-6 text-sm text-muted-foreground">{error}</p>
      <PrimaryButton onClick={onRetry} variant="default">
        <RefreshCw className="mr-2 h-4 w-4" />
        Try Again
      </PrimaryButton>
    </div>
  );
};
