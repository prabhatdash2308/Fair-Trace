import * as React from 'react';
import { FileUploader } from '@/components/upload';
import { uploadApi } from '@/api/upload.api';

export const ReviewDocumentsTab: React.FC = () => {
  const [isUploading, setIsUploading] = React.useState(false);
  const [uploadedFiles, setUploadedFiles] = React.useState<any[]>([]);

  const handleUpload = async (files: FileList) => {
    if (files.length === 0) return;
    setIsUploading(true);
    try {
      // Just upload the first file for the happy path
      const res = await uploadApi.uploadFile(files[0]);
      setUploadedFiles(prev => [...prev, res.data]);
    } catch (err: any) {
      alert('Upload Failed: ' + err.message);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="space-y-6 fade-in">
      <h3 className="text-lg font-semibold tracking-tight">Supporting Documents</h3>
      <div className="p-6 rounded-lg border border-border/50 bg-card">
        <FileUploader 
          disabled={isUploading} 
          disabledMessage={isUploading ? "Uploading..." : "Upload disabled"}
          onUpload={handleUpload} 
        />
      </div>
      <div className="mt-6">
        <h4 className="text-sm font-medium mb-4">Uploaded Files</h4>
        {uploadedFiles.length === 0 ? (
          <div className="flex flex-col items-center justify-center p-8 rounded-lg border border-dashed border-border/50 bg-muted/10 text-center">
            <p className="text-sm font-medium mb-1">No documents uploaded.</p>
            <p className="text-xs text-muted-foreground">Upload performance reviews, 1on1 notes, or peer feedback to be analyzed by AI.</p>
          </div>
        ) : (
          <ul className="space-y-2">
            {uploadedFiles.map((f, i) => (
              <li key={i} className="p-3 border rounded text-sm bg-muted/20 flex justify-between">
                <span>{f.filename || 'Document'}</span>
                <span className="text-success text-xs">Ready</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};
