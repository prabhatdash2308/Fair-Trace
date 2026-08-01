import * as React from 'react';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { LoadingTable, BaseEmptyState } from '@/components/feedback';
import { cn } from '@/lib/utils';
import { FileText } from 'lucide-react';

export interface EnterpriseTableColumn<T> {
  header: React.ReactNode;
  accessorKey?: keyof T;
  cell?: (item: T) => React.ReactNode;
  className?: string;
}

export interface EnterpriseTableProps<T> {
  data: T[];
  columns: EnterpriseTableColumn<T>[];
  keyExtractor: (item: T) => string;
  isLoading?: boolean;
  emptyTitle?: string;
  emptyDescription?: string;
  onRowClick?: (item: T) => void;
  className?: string;
}

export function EnterpriseTable<T>({
  data,
  columns,
  keyExtractor,
  isLoading,
  emptyTitle = 'No data available',
  emptyDescription = 'There are no records to display.',
  onRowClick,
  className,
}: EnterpriseTableProps<T>) {
  if (isLoading) {
    return <LoadingTable rows={5} />;
  }

  if (data.length === 0) {
    return (
      <BaseEmptyState
        icon={FileText}
        title={emptyTitle}
        description={emptyDescription}
      />
    );
  }

  return (
    <div className={cn('rounded-md border bg-card', className)}>
      <Table>
        <TableHeader>
          <TableRow className="hover:bg-transparent">
            {columns.map((col, idx) => (
              <TableHead key={idx} className={col.className}>
                {col.header}
              </TableHead>
            ))}
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((item) => (
            <TableRow
              key={keyExtractor(item)}
              onClick={() => onRowClick?.(item)}
              className={cn(
                onRowClick && 'cursor-pointer hover:bg-muted/50 transition-colors',
                'group'
              )}
            >
              {columns.map((col, idx) => (
                <TableCell key={idx} className={col.className}>
                  {col.cell ? col.cell(item) : (item[col.accessorKey as keyof T] as React.ReactNode)}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
