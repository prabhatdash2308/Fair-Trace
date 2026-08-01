import * as React from 'react';
import { Search, FolderOpen, Users, FileText, Activity } from 'lucide-react';
import { cn } from '@/utils';
import { PrimaryButton } from '@/components/ui/PrimaryButton';

interface BaseEmptyStateProps {
  icon: React.ElementType;
  title: string;
  description: string;
  actionLabel?: string;
  onAction?: () => void;
  className?: string;
}

export const BaseEmptyState: React.FC<BaseEmptyStateProps> = ({
  icon: Icon,
  title,
  description,
  actionLabel,
  onAction,
  className,
}) => {
  return (
    <div className={cn('flex min-h-[300px] flex-col items-center justify-center text-center p-8 border border-dashed rounded-lg bg-muted/20', className)}>
      <div className="flex h-12 w-12 items-center justify-center rounded-full bg-muted/50 mb-4">
        <Icon className="h-6 w-6 text-muted-foreground" />
      </div>
      <h3 className="text-lg font-semibold text-foreground mb-1">{title}</h3>
      <p className="text-sm text-muted-foreground max-w-[250px] mb-6">{description}</p>
      {actionLabel && onAction && (
        <PrimaryButton onClick={onAction}>{actionLabel}</PrimaryButton>
      )}
    </div>
  );
};

export const EmptySearch = (props: Partial<BaseEmptyStateProps>) => (
  <BaseEmptyState
    icon={Search}
    title="No results found"
    description="We couldn't find anything matching your search. Try adjusting your filters."
    {...props}
  />
);

export const EmptyEmployees = (props: Partial<BaseEmptyStateProps>) => (
  <BaseEmptyState
    icon={Users}
    title="No employees found"
    description="Get started by adding your first employee to the platform."
    {...props}
  />
);

export const EmptyReviews = (props: Partial<BaseEmptyStateProps>) => (
  <BaseEmptyState
    icon={FolderOpen}
    title="No review cycles"
    description="There are currently no active review cycles for this period."
    {...props}
  />
);

export const EmptyReports = (props: Partial<BaseEmptyStateProps>) => (
  <BaseEmptyState
    icon={FileText}
    title="No reports generated"
    description="Performance reports will appear here once the AI pipeline completes."
    {...props}
  />
);

export const EmptyPipeline = (props: Partial<BaseEmptyStateProps>) => (
  <BaseEmptyState
    icon={Activity}
    title="Pipeline idle"
    description="Trigger the AI pipeline to analyze inputs and generate performance reports."
    {...props}
  />
);
