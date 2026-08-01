import * as React from 'react';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { cn } from '@/lib/utils';
import type { Employee } from '@/features/employees/types';

export interface ReviewerAvatarProps {
  employee: Employee | null;
  className?: string;
  showDetails?: boolean;
}

export const ReviewerAvatar: React.FC<ReviewerAvatarProps> = ({ employee, className, showDetails = false }) => {
  if (!employee) {
    return (
      <div className={cn("flex items-center gap-3", className)}>
        <Avatar className="h-8 w-8 border border-border/50 bg-muted/20">
          <AvatarFallback className="text-xs text-muted-foreground">?</AvatarFallback>
        </Avatar>
        {showDetails && (
          <div className="flex flex-col">
            <span className="text-sm font-medium text-muted-foreground">Unassigned</span>
          </div>
        )}
      </div>
    );
  }

  const initials = employee.full_name.substring(0, 2).toUpperCase();

  return (
    <div className={cn("flex items-center gap-3", className)}>
      <Avatar className="h-8 w-8 border border-border/50 bg-background shadow-sm">
        <AvatarImage src={`https://api.dicebear.com/7.x/initials/svg?seed=${employee.full_name}&backgroundColor=000000`} alt={employee.full_name} />
        <AvatarFallback className="text-xs">{initials}</AvatarFallback>
      </Avatar>
      {showDetails && (
        <div className="flex flex-col">
          <span className="text-sm font-medium leading-none">{employee.full_name}</span>
          <span className="text-xs text-muted-foreground mt-1">{employee.designation || employee.role}</span>
        </div>
      )}
    </div>
  );
};
