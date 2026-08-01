import * as React from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { EnterpriseTable, type EnterpriseTableColumn } from '@/components/tables';
import { ReviewStatus } from '@/components/status';
import { formatDate } from '@/utils';
import type { ReviewCycle } from '@/api';
import { useRecentActivity } from '../hooks/useDashboard';

export const ReviewQueue: React.FC = () => {
  const navigate = useNavigate();
  const { data = [], isLoading } = useRecentActivity(5);

  const columns: EnterpriseTableColumn<ReviewCycle>[] = [
    {
      header: 'Title',
      accessorKey: 'title',
      className: 'font-medium',
    },
    {
      header: 'Status',
      cell: (item) => <ReviewStatus status={item.status} />,
    },
    {
      header: 'Period',
      cell: (item) => (
        <span className="text-sm text-muted-foreground">
          {formatDate(item.review_period_start)} – {formatDate(item.review_period_end)}
        </span>
      ),
    },
  ];

  return (
    <Card className="h-full border-border/50 shadow-sm">
      <CardHeader className="pb-3 border-b border-border/50">
        <CardTitle className="text-base font-semibold">Recent Reviews</CardTitle>
      </CardHeader>
      <CardContent className="p-0">
        <EnterpriseTable
          data={data}
          columns={columns}
          keyExtractor={(item) => item.id}
          isLoading={isLoading}
          onRowClick={(item) => navigate(`/cycles/${item.id}`)}
          className="border-0 rounded-none shadow-none"
          emptyTitle="No recent reviews"
          emptyDescription="Create a review cycle to get started."
        />
      </CardContent>
    </Card>
  );
};
