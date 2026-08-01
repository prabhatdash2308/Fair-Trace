import * as React from 'react';
import { useNavigate } from 'react-router-dom';
import { EnterpriseTable, type EnterpriseTableColumn } from '@/components/tables';
import { ReviewerAvatar, ReviewStage, ScoreBadge } from '@/components/review';
import { ROUTES } from '@/constants/routes';
import { formatDate } from '@/utils';
import type { ReviewCycle } from '../types/review.types';
import { MoreHorizontal } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

export interface ReviewTableProps {
  data: ReviewCycle[];
  isLoading: boolean;
}

export const ReviewTable: React.FC<ReviewTableProps> = ({ data, isLoading }) => {
  const navigate = useNavigate();

  const columns: EnterpriseTableColumn<ReviewCycle>[] = [
    {
      header: 'Review Cycle',
      cell: (item) => (
        <div className="flex flex-col">
          <span className="font-medium text-foreground hover:underline cursor-pointer" onClick={() => navigate(ROUTES.reviewDetail(item.id))}>
            {item.title}
          </span>
          <span className="text-xs text-muted-foreground mt-0.5">
            {formatDate(item.review_period_start)} - {formatDate(item.review_period_end)}
          </span>
        </div>
      )
    },
    {
      header: 'Stage',
      cell: (item) => <ReviewStage status={item.status} />
    },
    {
      header: 'AI Status',
      cell: () => <span className="text-xs text-muted-foreground">Pending</span> // Mocked for now until backend provides it directly
    },
    {
      header: 'Overall Score',
      cell: () => <ScoreBadge score={null} /> // Mocked until AI payload provides score
    },
    {
      header: 'Updated',
      cell: (item) => <span className="text-sm">{formatDate(item.updated_at)}</span>
    },
    {
      header: '',
      cell: (item) => (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="h-8 w-8 p-0">
              <span className="sr-only">Open menu</span>
              <MoreHorizontal className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem onClick={() => navigate(ROUTES.reviewDetail(item.id))}>
              View Details
            </DropdownMenuItem>
            <DropdownMenuItem onClick={() => navigate(ROUTES.pipelineMonitor(item.id))}>
              View Pipeline
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      )
    }
  ];

  return (
    <EnterpriseTable 
      columns={columns} 
      data={data} 
      isLoading={isLoading} 
      keyExtractor={(item) => item.id}
      emptyTitle="No reviews found"
      emptyDescription="There are no review cycles matching your filters."
    />
  );
};
