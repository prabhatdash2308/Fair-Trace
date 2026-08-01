import * as React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { Loader2 } from 'lucide-react';

export interface ChartContainerProps extends React.HTMLAttributes<HTMLDivElement> {
  title?: string;
  description?: string;
  isLoading?: boolean;
  isEmpty?: boolean;
  emptyMessage?: string;
}

export const ChartContainer = React.forwardRef<HTMLDivElement, ChartContainerProps>(
  ({ className, title, description, isLoading, isEmpty, emptyMessage = 'No data available', children, ...props }, ref) => {
    return (
      <Card className={cn('overflow-hidden transition-all hover:shadow-floating border-border/50', className)} ref={ref} {...props}>
        {(title || description) && (
          <CardHeader className="pb-4">
            {title && <CardTitle className="text-base font-semibold">{title}</CardTitle>}
            {description && <p className="text-sm text-muted-foreground">{description}</p>}
          </CardHeader>
        )}
        <CardContent>
          {isLoading ? (
            <div className="flex h-[300px] w-full items-center justify-center">
              <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
            </div>
          ) : isEmpty ? (
            <div className="flex h-[300px] w-full flex-col items-center justify-center text-center">
              <div className="mb-2 h-10 w-10 rounded-full bg-muted/50 flex items-center justify-center">
                <span className="text-muted-foreground opacity-50">📉</span>
              </div>
              <p className="text-sm text-muted-foreground">{emptyMessage}</p>
            </div>
          ) : (
            <div className="h-[300px] w-full">
              {children}
            </div>
          )}
        </CardContent>
      </Card>
    );
  }
);
ChartContainer.displayName = 'ChartContainer';
