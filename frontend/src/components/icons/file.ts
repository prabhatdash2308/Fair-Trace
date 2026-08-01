import {
  File,
  FileText,
  FileSpreadsheet,
  Image as ImageIcon,
  Paperclip,
  Download,
  Upload,
  Folder,
  FolderOpen
} from 'lucide-react';

export const FileIcons = {
  Document: FileText,
  PDF: File,
  CSV: FileSpreadsheet,
  Image: ImageIcon,
  Attachment: Paperclip,
  Download,
  Upload,
  Folder,
  FolderOpen,
} as const;
