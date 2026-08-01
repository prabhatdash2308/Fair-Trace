import * as React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ShieldCheck } from 'lucide-react';
import { useDashboardKPIs } from '../hooks/useDashboard';

export const ApprovalQueue: React.FC = () => {
  const { data } = useDashboardKPIs();
  const hasApprovals = data?.pendingApprovals ? data.pendingApprovals > 0 : false;

  return (
    <Card className="h-full border-border/50 shadow-sm">
      <CardHeader className="pb-3 border-b border-border/50">
        <CardTitle className="text-base font-semibold flex items-center gap-2">
          <ShieldCheck className="h-4 w-4 text-muted-foreground" />
          Pending Approvals
        </CardTitle>
      </CardHeader>
      <CardContent className="pt-6">
        {hasApprovals ? (
          <div className="flex h-[200px] flex-col items-center justify-center text-center">
            <h3 className="text-lg font-medium">{data?.pendingApprovals} items</h3>
            <p className="text-sm text-muted-foreground mt-1">Awaiting your approval.</p>
          </div>
        ) : (
          <div className="flex h-[200px] flex-col items-center justify-center text-center">
            <div className="mb-2 flex h-10 w-10 items-center justify-center rounded-full bg-muted/50">
              <ShieldCheck className="h-5 w-5 text-muted-foreground opacity-50" />
            </div>
            <p className="text-sm text-muted-foreground">No pending approvals.</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
};
