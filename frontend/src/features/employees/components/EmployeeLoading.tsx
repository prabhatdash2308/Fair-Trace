import * as React from 'react';
import { LoadingTable } from '@/components/feedback';

export const EmployeeLoading: React.FC = () => {
  return (
    <div className="space-y-4 fade-in">
      <div className="h-10 w-full max-w-sm rounded-md bg-muted animate-pulse" />
      <LoadingTable rows={8} />
    </div>
  );
};
