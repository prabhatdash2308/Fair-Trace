import * as React from 'react';
import { FileUploader } from '@/components/upload';

export const ReviewDocumentsTab: React.FC = () => {
  return (
    <div className="space-y-6 fade-in">
      <h3 className="text-lg font-semibold tracking-tight">Supporting Documents</h3>
      <div className="p-6 rounded-lg border border-border/50 bg-card">
        {/* The uploader currently renders a disabled enterprise empty state per phase 5 rules */}
        <FileUploader />
      </div>
      <div className="mt-6">
        <h4 className="text-sm font-medium mb-4">Uploaded Files</h4>
        <div className="flex flex-col items-center justify-center p-8 rounded-lg border border-dashed border-border/50 bg-muted/10 text-center">
          <p className="text-sm font-medium mb-1">No documents uploaded.</p>
          <p className="text-xs text-muted-foreground">Upload performance reviews, 1on1 notes, or peer feedback to be analyzed by AI.</p>
        </div>
      </div>
    </div>
  );
};
