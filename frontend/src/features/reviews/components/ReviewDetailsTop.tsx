import * as React from 'react';
import { useNavigate } from 'react-router-dom';
import { ROUTES } from '@/constants/routes';
import { ReviewStage, ScoreBadge, ReviewerAvatar } from '@/components/review';
import { formatDate } from '@/utils';
import { ExternalLink } from 'lucide-react';
import type { ReviewCycle } from '../types/review.types';
import type { Employee } from '@/features/employees/types';

export interface ReviewDetailsTopProps {
  cycle: ReviewCycle;
  employee: Employee | null;
  pipelineStatus?: string; // e.g. 'RUNNING', 'COMPLETED'
}

export const ReviewDetailsTop: React.FC<ReviewDetailsTopProps> = ({ cycle, employee, pipelineStatus = 'PENDING' }) => {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col md:flex-row justify-between gap-6 p-6 rounded-xl border border-border/50 bg-card shadow-sm mb-6 fade-in">
      <div className="flex flex-col gap-4">
        <h2 className="text-xl font-bold tracking-tight">{cycle.title}</h2>
        
        <div className="flex flex-wrap items-center gap-6">
          <div className="flex flex-col gap-1">
            <span className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Employee</span>
            <div 
              className="flex items-center gap-2 cursor-pointer hover:bg-muted/50 p-1 -ml-1 rounded-md transition-colors"
              onClick={() => employee && navigate(ROUTES.employeeProfile(employee.id))}
            >
              <ReviewerAvatar employee={employee} showDetails={false} className="gap-2" />
              <span className="text-sm font-medium hover:underline">{employee?.full_name || 'Loading...'}</span>
              <ExternalLink className="h-3 w-3 text-muted-foreground" />
            </div>
          </div>

          {/* If we had a manager object, we'd render it similarly. For now, mocking manager. */}
          <div className="flex flex-col gap-1">
            <span className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Manager</span>
            <span className="text-sm font-medium mt-1">Jane Doe</span>
          </div>

          <div className="flex flex-col gap-1">
            <span className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Department</span>
            <span className="text-sm font-medium mt-1">{employee?.department || 'Engineering'}</span>
          </div>
        </div>
      </div>

      <div className="flex flex-wrap md:flex-nowrap items-start md:items-center gap-6 md:gap-8">
        <div className="flex flex-col gap-2 min-w-[120px]">
          <span className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Stage</span>
          <ReviewStage status={cycle.status} />
        </div>

        <div className="flex flex-col gap-2 min-w-[120px]">
          <span className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Pipeline</span>
          <div 
            className="flex items-center gap-1 cursor-pointer hover:underline text-sm font-medium text-blue-500"
            onClick={() => navigate(ROUTES.pipelineMonitor(cycle.id))}
          >
            {pipelineStatus} <ExternalLink className="h-3 w-3" />
          </div>
        </div>

        <div className="flex flex-col gap-2 min-w-[100px]">
          <span className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Score</span>
          <ScoreBadge score={null} />
        </div>

        <div className="flex flex-col gap-2 text-right hidden lg:flex">
          <span className="text-xs text-muted-foreground">Created: {formatDate(cycle.created_at)}</span>
          <span className="text-xs text-muted-foreground">Updated: {formatDate(cycle.updated_at)}</span>
        </div>
      </div>
    </div>
  );
};
