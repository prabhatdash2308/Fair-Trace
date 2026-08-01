import * as React from 'react';
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs';

export interface ReviewStatusTabsProps {
  activeStatus: string;
  onStatusChange: (status: string) => void;
}

export const ReviewStatusTabs: React.FC<ReviewStatusTabsProps> = ({ activeStatus, onStatusChange }) => {
  return (
    <Tabs value={activeStatus} onValueChange={onStatusChange} className="w-full mb-6">
      <TabsList className="bg-transparent h-10 p-0 space-x-6 border-b border-border/50 rounded-none w-full justify-start overflow-x-auto">
        {['ALL', 'ACTIVE', 'PROCESSING', 'PENDING_APPROVAL', 'COMPLETED'].map((status) => (
          <TabsTrigger 
            key={status} 
            value={status}
            className="data-[state=active]:bg-transparent data-[state=active]:shadow-none data-[state=active]:border-b-2 data-[state=active]:border-primary rounded-none px-1 h-10 text-sm capitalize"
          >
            {status.replace('_', ' ').toLowerCase()}
          </TabsTrigger>
        ))}
      </TabsList>
    </Tabs>
  );
};
