import * as React from 'react';
import { cn } from '@/lib/utils';
import { Download, Printer, Link, FileJson, ChevronDown } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"

export const ReportExportButton: React.FC = () => {
  return (
    <TooltipProvider>
      <DropdownMenu>
        <Tooltip>
          <TooltipTrigger asChild>
            <div className="inline-block cursor-not-allowed">
              <DropdownMenuTrigger asChild disabled>
                <Button variant="outline" className="h-9 gap-2 pointer-events-none opacity-50">
                  <Download className="h-4 w-4" />
                  Export
                  <ChevronDown className="h-3 w-3 opacity-50" />
                </Button>
              </DropdownMenuTrigger>
            </div>
          </TooltipTrigger>
          <TooltipContent side="bottom">
            <p>Available after backend integration.</p>
          </TooltipContent>
        </Tooltip>
        
        {/* Placeholder for future backend integration. Leaving TODO as requested. */}
        {/* TODO: Enable actions when useDownloadReport() API is implemented */}
        <DropdownMenuContent align="end" className="w-48">
          <DropdownMenuItem disabled>
            <Download className="mr-2 h-4 w-4" />
            Download PDF
          </DropdownMenuItem>
          <DropdownMenuItem disabled>
            <Printer className="mr-2 h-4 w-4" />
            Print
          </DropdownMenuItem>
          <DropdownMenuItem disabled>
            <Link className="mr-2 h-4 w-4" />
            Copy Link
          </DropdownMenuItem>
          <DropdownMenuItem disabled>
            <FileJson className="mr-2 h-4 w-4" />
            Download JSON
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </TooltipProvider>
  );
};
