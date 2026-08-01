import * as React from 'react';
import { UploadCloud } from 'lucide-react';
import { cn } from '@/lib/utils';
import { PrimaryButton } from '@/components/ui/PrimaryButton';

export interface FileUploaderProps {
  onUpload?: (files: FileList) => void;
  disabled?: boolean;
  disabledMessage?: string;
  acceptedFormats?: string;
  className?: string;
}

export const FileUploader: React.FC<FileUploaderProps> = ({
  onUpload,
  disabled = false,
  disabledMessage = 'Upload will be enabled when backend support is available',
  acceptedFormats = 'PDF, DOCX, TXT, Images',
  className,
}) => {
  const [isDragging, setIsDragging] = React.useState(false);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    if (!disabled) setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (!disabled && onUpload && e.dataTransfer.files) {
      onUpload(e.dataTransfer.files);
    }
  };

  return (
    <div
      className={cn(
        'relative flex flex-col items-center justify-center rounded-lg border-2 border-dashed p-8 transition-colors',
        disabled ? 'border-border/50 bg-muted/20 opacity-70' : 
        isDragging ? 'border-primary bg-primary/5' : 'border-border/50 hover:border-primary/50 hover:bg-muted/50',
        className
      )}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      <div className="flex h-12 w-12 items-center justify-center rounded-full bg-muted/50 mb-4">
        <UploadCloud className="h-6 w-6 text-muted-foreground" />
      </div>
      <h3 className="text-sm font-semibold mb-1">
        {disabled ? 'Upload Disabled' : 'Drag & drop files here'}
      </h3>
      <p className="text-xs text-muted-foreground text-center max-w-[250px] mb-4">
        {disabled ? disabledMessage : `Supported formats: ${acceptedFormats}`}
      </p>
      <PrimaryButton disabled={disabled}>
        Select Files
      </PrimaryButton>
    </div>
  );
};
