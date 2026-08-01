import * as React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { Loader2 } from 'lucide-react';

export interface MetricCardProps {
  title: string;
  value: string | number | null | undefined;
  icon?: React.ElementType;
  description?: string;
  trend?: {
    value: number;
    label: string;
    isPositive?: boolean;
  };
  isLoading?: boolean;
  className?: string;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  icon: Icon,
  description,
  trend,
  isLoading,
  className,
}) => {
  return (
    <Card className={cn('overflow-hidden transition-all hover:shadow-floating border-border/50', className)}>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">{title}</CardTitle>
        {Icon && <Icon className="h-4 w-4 text-muted-foreground" />}
      </CardHeader>
      <CardContent>
        {isLoading ? (
          <div className="flex h-8 items-center">
            <Loader2 className="h-5 w-5 animate-spin text-muted-foreground" />
          </div>
        ) : (
          <div className="text-2xl font-semibold tracking-tight text-foreground">
            {value != null ? value : '—'}
          </div>
        )}
        
        {(description || trend) && !isLoading && (
          <div className="mt-1 flex items-center text-xs">
            {trend && (
              <span
                className={cn(
                  'mr-2 font-medium',
                  trend.isPositive === true && 'text-success',
                  trend.isPositive === false && 'text-destructive',
                  trend.isPositive === undefined && 'text-muted-foreground'
                )}
              >
                {trend.value > 0 ? '+' : ''}{trend.value}%
              </span>
            )}
            <span className="text-muted-foreground">{trend?.label || description}</span>
          </div>
        )}
      </CardContent>
    </Card>
  );
};
