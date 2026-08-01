import * as React from 'react';

export const PipelineLoading: React.FC = () => {
  return (
    <div className="space-y-6 fade-in p-6">
      <div className="h-24 w-full rounded-md bg-muted animate-pulse" />
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="col-span-1 space-y-4">
          <div className="h-64 w-full rounded-md bg-muted animate-pulse" />
        </div>
        <div className="col-span-2 space-y-4">
          <div className="h-32 w-full rounded-md bg-muted animate-pulse" />
          <div className="h-64 w-full rounded-md bg-muted animate-pulse" />
        </div>
      </div>
    </div>
  );
};
