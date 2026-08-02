import * as React from 'react';
import type { Citation } from '@/features/reports/types/report.types';
import { Copy } from 'lucide-react';
import { useToast } from '@/components/ui/use-toast';

export const CitationCard: React.FC<{ citation: Citation }> = ({ citation }) => {
  const { toast } = useToast();

  const handleCopy = () => {
    navigator.clipboard.writeText(citation.extracted_passage);
    toast({ title: "Citation Copied" });
  };

  return (
    <div className="p-4 rounded-md border border-border/50 bg-card group">
      <div className="flex items-start justify-between gap-4 mb-2">
        <div className="flex items-center gap-3">
          <span className="inline-flex items-center rounded-md border bg-muted px-2 py-0.5 text-[10px] font-mono font-medium text-muted-foreground uppercase">
            SIM {(citation.similarity_score * 100).toFixed(1)}%
          </span>
          <span className="text-xs font-medium text-muted-foreground">Chunk #{citation.id.substring(0, 6)}</span>
        </div>
        <button 
          onClick={handleCopy}
          className="text-muted-foreground hover:text-foreground opacity-0 group-hover:opacity-100 transition-opacity"
        >
          <Copy className="h-3.5 w-3.5" />
        </button>
      </div>
      
      <p className="text-sm italic text-foreground/90 leading-relaxed mb-3">"{citation.extracted_passage}"</p>
      
      <div className="flex items-center gap-2 text-xs text-muted-foreground">
        <span>Source: <span className="font-medium hover:underline cursor-pointer">Input #{citation.review_input_id.substring(0, 6)}</span></span>
        <span>•</span>
        <span>Rank: {citation.retrieval_rank}</span>
      </div>
    </div>
  );
};
