import * as React from 'react';
import { EnterpriseTable, type EnterpriseTableColumn } from '@/components/tables';
import { ReportStatus, ReportVersionBadge } from '@/components/report';
import { formatDate } from '@/utils';
import type { Report } from '../types/report.types';
import { MoreHorizontal } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useNavigate } from 'react-router-dom';
import { ROUTES } from '@/constants/routes';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

export interface ReportsTableProps {
  data: Report[];
  isLoading: boolean;
}

export const ReportsTable: React.FC<ReportsTableProps> = ({ data, isLoading }) => {
  const navigate = useNavigate();

  const columns: EnterpriseTableColumn<Report>[] = [
    {
      header: 'Report',
      cell: (item) => (
        <div className="flex flex-col">
          <span 
            className="font-medium text-foreground hover:underline cursor-pointer" 
            onClick={() => navigate(ROUTES.reportDetail(item.id))}
          >
            Review Cycle #{item.review_cycle_id.substring(0, 8)}
          </span>
          <span className="text-xs text-muted-foreground mt-0.5">
            Generated {formatDate(item.generated_at)}
          </span>
        </div>
      )
    },
    {
      header: 'Status',
      cell: (item) => <ReportStatus status={item.status} />
    },
    {
      header: 'Version',
      cell: (item) => <ReportVersionBadge version={item.version} isCurrent={true} />
    },
    {
      header: 'Confidence',
      cell: (item) => (
        <span className="text-sm font-medium capitalize">
          {item.confidence_score?.toLowerCase() || 'Pending'}
        </span>
      )
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
            <DropdownMenuItem onClick={() => navigate(ROUTES.reportDetail(item.id))}>
              View Document
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
      emptyTitle="No reports available"
      emptyDescription="AI-generated reports will appear here once they are generated from the Review workspace."
    />
  );
};
