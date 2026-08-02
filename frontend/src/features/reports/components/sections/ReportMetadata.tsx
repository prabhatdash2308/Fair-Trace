import * as React from 'react';
import type { Report } from '../../types/report.types';
import { ReportStatus, ReportVersionBadge, ReportExportButton } from '@/components/report';
import { formatDate } from '@/utils';
import { ExternalLink } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { ROUTES } from '@/constants/routes';

export const ReportMetadata: React.FC<{ report: Report }> = ({ report }) => {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 pb-8 border-b border-border/50">
      <div className="flex flex-col gap-2">
        <h1 className="text-3xl font-bold tracking-tight">AI Performance Report</h1>
        <div className="flex items-center gap-3 text-sm text-muted-foreground">
          <ReportVersionBadge version={report.version} isCurrent={true} />
          <span>Generated {formatDate(report.generated_at)}</span>
        </div>
      </div>

      <div className="flex items-center gap-4">
        {/* Deep Links mapping */}
        <div className="flex flex-col items-end gap-1 text-sm mr-4">
          <button 
            className="flex items-center gap-1 hover:underline text-muted-foreground"
            onClick={() => navigate(ROUTES.reviewDetail(report.review_cycle_id))}
          >
            Review Cycle <ExternalLink className="h-3 w-3" />
          </button>
          <button 
            className="flex items-center gap-1 hover:underline text-muted-foreground"
            onClick={() => navigate(ROUTES.pipelineMonitor(report.review_cycle_id))}
          >
            Pipeline Run <ExternalLink className="h-3 w-3" />
          </button>
        </div>
        
        <ReportStatus status={report.status} />
        <ReportExportButton reportId={report.id} />
      </div>
    </div>
  );
};
