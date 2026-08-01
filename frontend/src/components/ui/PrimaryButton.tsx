import * as React from 'react';
import { Button, type ButtonProps } from '@/components/ui/button';
import { cn } from '@/utils';

export const PrimaryButton = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, ...props }, ref) => {
    return (
      <Button
        ref={ref}
        variant="default"
        className={cn('font-medium shadow-sm transition-all hover:shadow-md active:scale-[0.98]', className)}
        {...props}
      />
    );
  }
);
PrimaryButton.displayName = 'PrimaryButton';
