import * as React from 'react';
import { PageToolbar } from '@/components/layout';
import { PrimaryButton } from '@/components/ui/PrimaryButton';
import { Plus } from 'lucide-react';
import { useAuthStore } from '@/store';

export const EmployeeHeader: React.FC = () => {
  const { user } = useAuthStore();
  const isAdmin = user?.role === 'ADMIN';

  return (
    <PageToolbar
      title="Employees"
      description="Manage your workforce, review history, and performance."
      actions={
        isAdmin ? (
          <PrimaryButton>
            <Plus className="mr-2 h-4 w-4" />
            Add Employee
          </PrimaryButton>
        ) : undefined
      }
      className="mb-6"
    />
  );
};
