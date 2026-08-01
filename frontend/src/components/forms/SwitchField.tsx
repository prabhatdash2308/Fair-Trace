import * as React from 'react';
import { cn } from '@/utils';

export interface SwitchFieldProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {
  label?: string;
  description?: string;
}

export const SwitchField = React.forwardRef<HTMLInputElement, SwitchFieldProps>(
  ({ className, label, description, id, ...props }, ref) => {
    const generatedId = React.useId();
    const fieldId = id || generatedId;

    return (
      <div className={cn('flex flex-row items-center justify-between rounded-lg border p-4', className)}>
        <div className="space-y-0.5">
          {label && (
            <label htmlFor={fieldId} className="text-base font-medium">
              {label}
            </label>
          )}
          {description && (
            <p className="text-sm text-muted-foreground">
              {description}
            </p>
          )}
        </div>
        <div className="relative inline-flex h-[24px] w-[44px] shrink-0 cursor-pointer items-center rounded-full border-2 border-transparent transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background disabled:cursor-not-allowed disabled:opacity-50">
          <input
            type="checkbox"
            id={fieldId}
            ref={ref}
            className="peer absolute inset-0 h-full w-full cursor-pointer appearance-none rounded-full bg-input checked:bg-primary focus-visible:outline-none disabled:cursor-not-allowed"
            {...props}
          />
          <span className="pointer-events-none block h-5 w-5 rounded-full bg-background shadow-lg ring-0 transition-transform peer-checked:translate-x-5" />
        </div>
      </div>
    );
  }
);
SwitchField.displayName = 'SwitchField';
