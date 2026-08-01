import * as React from 'react';
import { SearchField } from '@/components/forms';

export interface EmployeeToolbarProps {
  onSearchChange: (val: string) => void;
  searchValue: string;
}

export const EmployeeToolbar: React.FC<EmployeeToolbarProps> = ({ onSearchChange, searchValue }) => {
  return (
    <div className="flex flex-col sm:flex-row items-center justify-between gap-4 mb-4">
      <div className="w-full sm:max-w-sm">
        <SearchField 
          placeholder="Search by name, email or ID..."
          value={searchValue}
          onChange={(e) => onSearchChange(e.target.value)}
        />
      </div>
      <div className="flex items-center gap-2">
        {/* We can place generic filters here if needed */}
      </div>
    </div>
  );
};
