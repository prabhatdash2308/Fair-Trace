import * as React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Clock } from 'lucide-react';

export const ActivityFeed: React.FC = () => {
  // Activity feed endpoint is not built out fully in backend yet. 
  // We fall back to empty state to avoid mocking.
  return (
    <Card className="h-full border-border/50 shadow-sm">
      <CardHeader className="pb-3 border-b border-border/50">
        <CardTitle className="text-base font-semibold flex items-center gap-2">
          <Clock className="h-4 w-4 text-muted-foreground" />
          Recent Activity
        </CardTitle>
      </CardHeader>
      <CardContent className="pt-6">
        <div className="flex h-[200px] flex-col items-center justify-center text-center">
          <div className="mb-2 flex h-10 w-10 items-center justify-center rounded-full bg-muted/50">
            <Clock className="h-5 w-5 text-muted-foreground opacity-50" />
          </div>
          <p className="text-sm text-muted-foreground">No recent activity to display.</p>
        </div>
      </CardContent>
    </Card>
  );
};
