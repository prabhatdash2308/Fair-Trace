import * as React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { IconButton } from '@/components/ui/IconButton';
import { Download, Eye, Trash2, FileText, FileImage, FileBarChart } from 'lucide-react';
import { cn } from '@/lib/utils';
import { formatDate } from '@/utils';

export interface DocumentCardProps {
  id: string;
  name: string;
  type: 'PDF' | 'DOCX' | 'TXT' | 'IMAGE';
  category: 'Self Assessment' | 'Peer Review' | 'Manager Review' | 'Goals' | 'Supporting';
  uploadedAt: string;
  sizeBytes?: number;
  onPreview?: (id: string) => void;
  onDownload?: (id: string) => void;
  onDelete?: (id: string) => void;
  className?: string;
}

export const DocumentCard: React.FC<DocumentCardProps> = ({
  id,
  name,
  type,
  category,
  uploadedAt,
  sizeBytes,
  onPreview,
  onDownload,
  onDelete,
  className,
}) => {
  const FileIcon = type === 'PDF' ? FileText :
                   type === 'IMAGE' ? FileImage : 
                   FileBarChart;

  const sizeStr = sizeBytes ? `${(sizeBytes / 1024).toFixed(1)} KB` : '';

  return (
    <Card className={cn('overflow-hidden border-border/50 shadow-sm transition-all hover:shadow-floating hover:border-border group', className)}>
      <CardContent className="p-4 flex items-center gap-4">
        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-muted/50">
          <FileIcon className="h-5 w-5 text-muted-foreground" />
        </div>
        <div className="flex flex-1 flex-col overflow-hidden">
          <span className="truncate text-sm font-medium text-foreground" title={name}>{name}</span>
          <div className="flex items-center gap-2 mt-0.5 text-xs text-muted-foreground">
            <span className="inline-flex items-center rounded-sm bg-muted px-1.5 py-0.5 text-[10px] font-medium uppercase tracking-wider">
              {category}
            </span>
            <span>•</span>
            <span>{formatDate(uploadedAt)}</span>
            {sizeStr && (
              <>
                <span>•</span>
                <span>{sizeStr}</span>
              </>
            )}
          </div>
        </div>
        <div className="flex shrink-0 items-center gap-1 opacity-0 transition-opacity group-hover:opacity-100">
          {onPreview && (
            <IconButton icon={Eye} variant="secondary" onClick={() => onPreview(id)} title="Preview" />
          )}
          {onDownload && (
            <IconButton icon={Download} variant="secondary" onClick={() => onDownload(id)} title="Download" />
          )}
          {onDelete && (
            <IconButton icon={Trash2} variant="destructive" onClick={() => onDelete(id)} title="Delete" />
          )}
        </div>
      </CardContent>
    </Card>
  );
};
