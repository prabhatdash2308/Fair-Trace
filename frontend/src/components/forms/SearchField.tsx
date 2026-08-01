import * as React from 'react';
import { NavIcons, ActionIcons } from '@/components/icons';
import { Input } from '@/components/ui/input';
import { cn } from '@/utils';

export interface SearchFieldProps extends React.InputHTMLAttributes<HTMLInputElement> {
  onClear?: () => void;
}

export const SearchField = React.forwardRef<HTMLInputElement, SearchFieldProps>(
  ({ className, onClear, value, onChange, ...props }, ref) => {
    const { Search } = NavIcons;
    const { Cancel } = ActionIcons;

    return (
      <div className={cn('relative', className)}>
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <Input
          ref={ref}
          className="pl-9 pr-9"
          type="search"
          value={value}
          onChange={onChange}
          {...props}
        />
        {value && onClear && (
          <button
            type="button"
            onClick={onClear}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground focus:outline-none"
          >
            <Cancel className="h-4 w-4" />
          </button>
        )}
      </div>
    );
  }
);
SearchField.displayName = 'SearchField';
