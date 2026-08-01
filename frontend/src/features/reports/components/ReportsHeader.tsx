import * as React from 'react';
import { PageToolbar } from '@/components/layout';

export const ReportsHeader: React.FC = () => {
  return (
    <PageToolbar
      title="Executive Reports"
      description="View, compare, and approve AI-generated performance reports."
      className="mb-6"
    />
  );
};
