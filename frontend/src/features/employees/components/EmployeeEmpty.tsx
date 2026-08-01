import * as React from 'react';
import { BaseEmptyState } from '@/components/feedback';
import { Users } from 'lucide-react';

export const EmployeeEmpty: React.FC = () => {
  return (
    <BaseEmptyState 
      icon={Users}
      title="No employees found"
      description="It looks like there are no employees in the system matching your criteria."
    />
  );
};
