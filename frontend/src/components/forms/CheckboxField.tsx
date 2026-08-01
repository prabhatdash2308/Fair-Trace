import * as React from 'react';
import { cn } from '@/utils';
import { ActionIcons } from '@/components/icons';

export interface CheckboxFieldProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {
  label?: React.ReactNode;
  description?: string;
  error?: string;
}

export const CheckboxField = React.forwardRef<HTMLInputElement, CheckboxFieldProps>(
  ({ className, label, description, error, id, ...props }, ref) => {
    const generatedId = React.useId();
    const fieldId = id || generatedId;
    const { Confirm } = ActionIcons;

    return (
      <div className={cn('items-top flex space-x-2', className)}>
        <div className="relative flex items-center justify-center pt-0.5">
          <input
            type="checkbox"
            id={fieldId}
            ref={ref}
            className={cn(
              'peer h-4 w-4 shrink-0 appearance-none rounded-sm border border-primary ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
              'checked:bg-primary checked:text-primary-foreground',
              error && 'border-destructive checked:bg-destructive'
            )}
            {...props}
          />
          <Confirm className="pointer-events-none absolute hidden h-3 w-3 text-primary-foreground peer-checked:block" strokeWidth={3} />
        </div>
        <div className="grid gap-1.5 leading-none">
          {label && (
            <label
              htmlFor={fieldId}
              className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
            >
              {label}
            </label>
          )}
          {description && (
            <p className="text-sm text-muted-foreground">
              {description}
            </p>
          )}
          {error && (
            <p className="text-sm font-medium text-destructive">{error}</p>
          )}
        </div>
      </div>
    );
  }
);
CheckboxField.displayName = 'CheckboxField';
