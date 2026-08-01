import * as React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { cn } from '@/lib/utils';
import type { Employee } from '@/features/employees/types';

export interface EmployeeSummaryCardProps {
  employee: Employee;
  className?: string;
  onClick?: () => void;
}

export const EmployeeSummaryCard: React.FC<EmployeeSummaryCardProps> = ({
  employee,
  className,
  onClick,
}) => {
  const initials = employee.full_name
    .split(' ')
    .map((n: string) => n[0])
    .join('')
    .substring(0, 2)
    .toUpperCase();

  return (
    <Card 
      className={cn(
        'overflow-hidden border-border/50 shadow-sm transition-all',
        onClick && 'cursor-pointer hover:shadow-floating hover:border-border',
        className
      )}
      onClick={onClick}
    >
      <CardContent className="p-4 flex items-center gap-4">
        <Avatar className="h-12 w-12 border border-border/50">
          <AvatarImage src={`https://api.dicebear.com/7.x/initials/svg?seed=${employee.full_name}&backgroundColor=transparent&textColor=var(--foreground)`} />
          <AvatarFallback className="bg-muted text-muted-foreground">{initials}</AvatarFallback>
        </Avatar>
        <div className="flex flex-col">
          <span className="text-sm font-semibold text-foreground">{employee.full_name}</span>
          <span className="text-xs text-muted-foreground">{employee.designation || 'Employee'}</span>
          <span className="text-xs text-muted-foreground mt-0.5">{employee.department || 'General'}</span>
        </div>
      </CardContent>
    </Card>
  );
};
