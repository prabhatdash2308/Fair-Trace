import * as React from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus } from 'lucide-react';
import { useAuthStore } from '@/store';
import { PageToolbar } from '@/components/layout';
import { PrimaryButton } from '@/components/ui/PrimaryButton';

export const DashboardHeader: React.FC = () => {
  const { user } = useAuthStore();
  const navigate = useNavigate();

  const isManagerOrAdmin = user?.role === 'MANAGER' || user?.role === 'ADMIN';

  const actions = isManagerOrAdmin ? (
    <PrimaryButton onClick={() => navigate('/cycles/new')}>
      <Plus className="mr-2 h-4 w-4" />
      New Review Cycle
    </PrimaryButton>
  ) : undefined;

  return (
    <PageToolbar
      title="Dashboard"
      description={`Welcome back, ${user?.full_name || 'User'} — ${user?.role || 'EMPLOYEE'}`}
      actions={actions}
      className="mb-8"
    />
  );
};
