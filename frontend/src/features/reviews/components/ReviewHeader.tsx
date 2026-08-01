import * as React from 'react';
import { PageToolbar } from '@/components/layout';
import { PrimaryButton } from '@/components/ui/PrimaryButton';
import { Plus } from 'lucide-react';

export interface ReviewHeaderProps {
  onCreateClick: () => void;
}

export const ReviewHeader: React.FC<ReviewHeaderProps> = ({ onCreateClick }) => {
  return (
    <PageToolbar
      title="Review Cycles"
      description="Manage enterprise performance reviews and AI evaluations."
      actions={
        <PrimaryButton onClick={onCreateClick}>
          <Plus className="mr-2 h-4 w-4" />
          Create Review
        </PrimaryButton>
      }
      className="mb-6"
    />
  );
};
