import * as React from 'react';
import { useNavigate } from 'react-router-dom';
import { EnterpriseTable, type EnterpriseTableColumn } from '@/components/tables';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { EmployeeStatus } from '@/components/status';
import { formatDate } from '@/utils';
import { MoreHorizontal } from 'lucide-react';
import type { Employee } from '../types';

export interface EmployeeTableProps {
  data: Employee[];
  isLoading: boolean;
}

export const EmployeeTable: React.FC<EmployeeTableProps> = ({ data, isLoading }) => {
  const navigate = useNavigate();

  const columns: EnterpriseTableColumn<Employee>[] = [
    {
      header: 'Employee',
      cell: (item) => {
        const initials = item.full_name.substring(0, 2).toUpperCase();
        return (
          <div className="flex items-center gap-3 py-1">
            <Avatar className="h-9 w-9 border border-border/50">
              <AvatarImage src={`https://api.dicebear.com/7.x/initials/svg?seed=${item.full_name}&backgroundColor=transparent&textColor=var(--foreground)`} />
              <AvatarFallback className="bg-muted text-muted-foreground text-xs">{initials}</AvatarFallback>
            </Avatar>
            <div className="flex flex-col">
              <span className="font-medium">{item.full_name}</span>
              <span className="text-xs text-muted-foreground">{item.email}</span>
            </div>
          </div>
        );
      }
    },
    {
      header: 'Department',
      accessorKey: 'department',
      cell: (item) => <span className="text-sm">{item.department || '—'}</span>
    },
    {
      header: 'Role',
      accessorKey: 'role',
      cell: (item) => (
        <span className="inline-flex items-center rounded-sm bg-muted px-2 py-0.5 text-xs font-medium uppercase tracking-wider text-muted-foreground">
          {item.role}
        </span>
      )
    },
    {
      header: 'Manager',
      cell: (item) => <span className="text-sm text-muted-foreground">{item.manager_id ? 'Assigned' : '—'}</span>
    },
    {
      header: 'Status',
      cell: (item) => <EmployeeStatus isActive={item.is_active} />
    },
    {
      header: 'Joined',
      cell: (item) => <span className="text-sm text-muted-foreground">{formatDate(item.created_at)}</span>
    },
    {
      header: '',
      className: 'w-[40px]',
      cell: () => (
        <button className="flex h-8 w-8 items-center justify-center rounded-md hover:bg-muted text-muted-foreground transition-colors" onClick={(e) => e.stopPropagation()}>
          <MoreHorizontal className="h-4 w-4" />
        </button>
      )
    }
  ];

  return (
    <EnterpriseTable
      data={data}
      columns={columns}
      keyExtractor={(item) => item.id}
      isLoading={isLoading}
      onRowClick={(item) => navigate(`/employees/${item.id}`)}
      emptyTitle="No employees found"
      emptyDescription="Adjust your search filters or add a new employee."
      className="shadow-sm border-border/50"
    />
  );
};
