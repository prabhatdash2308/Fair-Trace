import * as React from 'react';
import { EnterpriseTable, type EnterpriseTableColumn } from '@/components/tables';
import { ReviewStatus } from '@/components/status';
import { formatDate } from '@/utils';
import type { ReviewCycle } from '@/api';

export const EmployeeReviews: React.FC = () => {
  // Hardcoded to empty list to avoid faking data until connected to actual user reviews endpoint.
  const data: ReviewCycle[] = [];
  const isLoading = false;

  const columns: EnterpriseTableColumn<ReviewCycle>[] = [
    {
      header: 'Cycle',
      accessorKey: 'title',
      className: 'font-medium',
    },
    {
      header: 'Status',
      cell: (item) => <ReviewStatus status={item.status} />
    },
    {
      header: 'Start Date',
      cell: (item) => <span className="text-sm text-muted-foreground">{formatDate(item.review_period_start)}</span>
    },
    {
      header: 'End Date',
      cell: (item) => <span className="text-sm text-muted-foreground">{formatDate(item.review_period_end)}</span>
    }
  ];

  return (
    <div className="space-y-6 fade-in">
      <h3 className="text-lg font-semibold tracking-tight">Review History</h3>
      <EnterpriseTable
        data={data}
        columns={columns}
        keyExtractor={(item) => item.id}
        isLoading={isLoading}
        emptyTitle="No reviews found"
        emptyDescription="This employee has not participated in any review cycles yet."
        className="shadow-sm border-border/50"
      />
    </div>
  );
};
