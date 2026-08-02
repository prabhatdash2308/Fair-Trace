import * as React from 'react';
import { Copy } from 'lucide-react';
import { useToast } from '@/components/ui/use-toast';

export const ExplainabilityJSON: React.FC<{ data: any }> = ({ data }) => {
  const { toast } = useToast();
  
  const handleCopy = () => {
    navigator.clipboard.writeText(JSON.stringify(data, null, 2));
    toast({ title: "JSON Copied", description: "Raw execution trace copied to clipboard." });
  };

  return (
    <div className="rounded-md border border-border/50 bg-[#0d0d0d] overflow-hidden">
      <div className="flex items-center justify-between px-4 py-2 border-b border-border/20 bg-muted/5">
        <span className="text-xs font-mono text-muted-foreground">execution_trace.json</span>
        <button 
          onClick={handleCopy}
          className="text-muted-foreground hover:text-foreground transition-colors p-1 rounded-md hover:bg-muted/20"
          title="Copy JSON"
        >
          <Copy className="h-3.5 w-3.5" />
        </button>
      </div>
      <div className="p-4 overflow-x-auto max-h-[400px] overflow-y-auto">
        <pre className="text-xs font-mono text-foreground/80 whitespace-pre-wrap">
          {JSON.stringify(data, null, 2)}
        </pre>
      </div>
    </div>
  );
};
