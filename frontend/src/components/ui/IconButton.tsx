import * as React from 'react';
import { Button, type ButtonProps } from '@/components/ui/button';
import { cn } from '@/utils';

export interface IconButtonProps extends ButtonProps {
  icon: React.ElementType;
  iconProps?: React.ComponentProps<'svg'>;
}

export const IconButton = React.forwardRef<HTMLButtonElement, IconButtonProps>(
  ({ className, icon: Icon, iconProps, ...props }, ref) => {
    return (
      <Button
        ref={ref}
        variant="ghost"
        size="icon"
        className={cn('transition-colors hover:bg-muted active:scale-[0.95]', className)}
        {...props}
      >
        <Icon className={cn('h-4 w-4', iconProps?.className)} {...iconProps} />
      </Button>
    );
  }
);
IconButton.displayName = 'IconButton';
