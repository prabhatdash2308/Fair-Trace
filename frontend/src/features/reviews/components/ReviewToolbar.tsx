import * as React from 'react';
import { Search } from 'lucide-react';
import { Input } from '@/components/ui/input';

export interface ReviewToolbarProps {
  searchTerm: string;
  onSearchChange: (value: string) => void;
}

export const ReviewToolbar: React.FC<ReviewToolbarProps> = ({ searchTerm, onSearchChange }) => {
  return (
    <div className="flex flex-col sm:flex-row items-center justify-between gap-4 py-4">
      <div className="relative w-full max-w-sm">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        <Input 
          placeholder="Search reviews..." 
          value={searchTerm}
          onChange={(e) => onSearchChange(e.target.value)}
          className="pl-9"
        />
      </div>
      {/* Additional filters can go here */}
    </div>
  );
};
