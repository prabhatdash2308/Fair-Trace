import * as React from 'react';
import { FileUploader } from '@/components/upload';
import { DocumentCard } from '@/components/document';
import { ResponsiveGrid } from '@/components/layout';

export const EmployeeDocuments: React.FC = () => {
  return (
    <div className="space-y-8 fade-in">
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
        <div>
          <h3 className="text-lg font-semibold tracking-tight">Documents</h3>
          <p className="text-sm text-muted-foreground">Upload and manage employee performance documents.</p>
        </div>
      </div>

      <FileUploader 
        disabled={true} 
        disabledMessage="Uploads will be enabled when backend support is fully integrated."
      />

      <div className="space-y-4">
        <h4 className="text-sm font-semibold tracking-tight text-muted-foreground uppercase">Uploaded Files</h4>
        <ResponsiveGrid columns={2}>
           {/* No fake documents per constraints. Show empty state handled by parent or just empty grid. */}
        </ResponsiveGrid>
        <div className="flex h-32 w-full flex-col items-center justify-center text-center rounded-lg border border-dashed border-border/50 bg-muted/20">
          <p className="text-sm text-muted-foreground">No documents uploaded yet.</p>
        </div>
      </div>
    </div>
  );
};
