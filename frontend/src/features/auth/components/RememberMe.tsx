import { cn } from '@/lib/utils';
import type { InputHTMLAttributes } from 'react';

interface RememberMeProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'type'> {
  id?: string;
}

/**
 * RememberMe — accessible checkbox with label.
 */
export function RememberMe({ id = 'remember-me', className, ...props }: RememberMeProps) {
  return (
    <div className={cn('flex items-center gap-2', className)}>
      <input
        id={id}
        type="checkbox"
        className={cn(
          'h-4 w-4 rounded border-border bg-background',
          'text-primary focus:ring-primary focus:ring-offset-background',
          'accent-primary cursor-pointer'
        )}
        {...props}
      />
      <label
        htmlFor={id}
        className="text-sm text-foreground cursor-pointer select-none"
      >
        Remember me
      </label>
    </div>
  );
}
