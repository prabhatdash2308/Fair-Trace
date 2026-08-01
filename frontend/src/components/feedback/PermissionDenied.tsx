import * as React from 'react';
import { ShieldAlert } from 'lucide-react';
import { PrimaryButton } from '@/components/ui/PrimaryButton';

interface PermissionDeniedProps {
  message?: string;
  onGoBack?: () => void;
}

export const PermissionDenied: React.FC<PermissionDeniedProps> = ({ 
  message = "You don't have permission to access this resource.",
  onGoBack
}) => {
  return (
    <div className="flex min-h-[400px] flex-col items-center justify-center space-y-4 text-center">
      <div className="flex h-16 w-16 items-center justify-center rounded-full bg-destructive/10">
        <ShieldAlert className="h-8 w-8 text-destructive" />
      </div>
      <div className="space-y-2">
        <h2 className="text-2xl font-semibold tracking-tight">Access Denied</h2>
        <p className="text-sm text-muted-foreground">{message}</p>
      </div>
      {onGoBack && (
        <PrimaryButton onClick={onGoBack} variant="outline">
          Go Back
        </PrimaryButton>
      )}
    </div>
  );
};
