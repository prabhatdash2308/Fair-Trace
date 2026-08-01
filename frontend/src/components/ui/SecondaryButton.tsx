import * as React from 'react';
import { Button, type ButtonProps } from '@/components/ui/button';
import { cn } from '@/utils';

export const SecondaryButton = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, ...props }, ref) => {
    return (
      <Button
        ref={ref}
        variant="secondary"
        className={cn('font-medium transition-all active:scale-[0.98]', className)}
        {...props}
      />
    );
  }
);
SecondaryButton.displayName = 'SecondaryButton';
