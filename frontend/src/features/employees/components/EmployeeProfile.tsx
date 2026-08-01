import * as React from 'react';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { EmployeeStatus } from '@/components/status';
import type { Employee } from '../types';

export const EmployeeProfile: React.FC<{ employee: Employee }> = ({ employee }) => {
  const initials = employee.full_name.substring(0, 2).toUpperCase();

  return (
    <div className="relative overflow-hidden rounded-xl border border-border/50 bg-gradient-to-b from-muted/30 to-background p-8 shadow-sm">
      <div className="absolute top-0 right-0 p-6">
        <EmployeeStatus isActive={employee.is_active} />
      </div>
      <div className="flex flex-col sm:flex-row items-center sm:items-start gap-6">
        <Avatar className="h-24 w-24 border-4 border-background shadow-sm">
          <AvatarImage src={`https://api.dicebear.com/7.x/initials/svg?seed=${employee.full_name}&backgroundColor=transparent&textColor=var(--foreground)`} />
          <AvatarFallback className="bg-muted text-muted-foreground text-2xl">{initials}</AvatarFallback>
        </Avatar>
        <div className="flex flex-col items-center sm:items-start text-center sm:text-left mt-2 sm:mt-0">
          <h1 className="text-2xl font-bold tracking-tight text-foreground">{employee.full_name}</h1>
          <p className="text-lg text-muted-foreground">{employee.designation || 'Team Member'}</p>
          <div className="mt-4 flex items-center gap-4 text-sm text-muted-foreground">
            <span className="flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-border"></span>
              {employee.department || 'General'} Department
            </span>
            <span>•</span>
            <span>{employee.email}</span>
          </div>
        </div>
      </div>
    </div>
  );
};
