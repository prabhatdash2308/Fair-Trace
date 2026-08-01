import * as React from 'react';
import { CheckCircle2 } from 'lucide-react';
import { cn } from '@/utils';

interface SuccessBannerProps {
  title: string;
  message?: string;
  className?: string;
}

export const SuccessBanner: React.FC<SuccessBannerProps> = ({ title, message, className }) => {
  return (
    <div className={cn('flex items-start gap-3 rounded-lg border border-success/20 bg-success/10 p-4', className)}>
      <CheckCircle2 className="mt-0.5 h-5 w-5 text-success shrink-0" />
      <div>
        <h4 className="text-sm font-semibold text-foreground">{title}</h4>
        {message && <p className="mt-1 text-sm text-muted-foreground">{message}</p>}
      </div>
    </div>
  );
};
