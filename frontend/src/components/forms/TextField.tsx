import * as React from 'react';
import { Input } from '@/components/ui/input';
import { cn } from '@/utils';

export interface TextFieldProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  hint?: string;
}

export const TextField = React.forwardRef<HTMLInputElement, TextFieldProps>(
  ({ label, error, hint, className, id, ...props }, ref) => {
    const generatedId = React.useId();
    const fieldId = id || generatedId;

    return (
      <div className={cn('space-y-2', className)}>
        {label && (
          <label
            htmlFor={fieldId}
            className="text-sm font-medium leading-none text-foreground peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
          >
            {label}
          </label>
        )}
        <Input
          id={fieldId}
          ref={ref}
          className={cn(error && 'border-destructive focus-visible:ring-destructive')}
          {...props}
        />
        {hint && !error && (
          <p className="text-[0.8rem] text-muted-foreground">{hint}</p>
        )}
        {error && (
          <p className="text-[0.8rem] font-medium text-destructive">{error}</p>
        )}
      </div>
    );
  }
);
TextField.displayName = 'TextField';
