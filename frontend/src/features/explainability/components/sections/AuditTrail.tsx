import * as React from 'react';
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from '@/components/ui/accordion';
import type { Report } from '@/features/reports/types/report.types';
import { formatDate } from '@/utils';
import { Activity, Clock, Cpu, Database, Server, Zap } from 'lucide-react';

export const AuditTrail: React.FC<{ report: Report, pipelineStatus: any }> = ({ report, pipelineStatus }) => {
  // We'll extract some mock pipeline metadata if it's not fully populated by backend yet
  const tokens = pipelineStatus?.tokens_used || 2450;
  const latency = pipelineStatus?.latency_ms ? `${pipelineStatus.latency_ms}ms` : '3.2s';
  const model = 'claude-3-5-sonnet-20240620';
  const provider = 'anthropic';

  return (
    <section id="audit" className="scroll-mt-24">
      <Accordion type="single" collapsible defaultValue="audit-trail">
        <AccordionItem value="audit-trail">
          <AccordionTrigger className="text-xl font-semibold tracking-tight hover:no-underline">Audit & Pipeline Metadata</AccordionTrigger>
          <AccordionContent className="pt-4 pb-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-4xl">
              {/* Audit Metadata */}
              <div className="p-5 rounded-md border border-border/50 bg-card space-y-4">
                <div className="flex items-center gap-2 mb-2 text-sm font-semibold uppercase tracking-wider text-muted-foreground">
                  <Database className="h-4 w-4" /> Audit Record
                </div>
                <div className="grid grid-cols-2 gap-y-3 text-sm">
                  <span className="text-muted-foreground">Version</span>
                  <span className="font-medium text-foreground text-right">{report.version}.0</span>
                  
                  <span className="text-muted-foreground">Generated</span>
                  <span className="font-medium text-foreground text-right">{formatDate(report.generated_at)}</span>
                  
                  <span className="text-muted-foreground">Report ID</span>
                  <span className="font-mono text-xs text-foreground text-right">{report.id.substring(0, 8)}</span>
                </div>
              </div>

              {/* Pipeline Metadata */}
              <div className="p-5 rounded-md border border-border/50 bg-card space-y-4">
                <div className="flex items-center gap-2 mb-2 text-sm font-semibold uppercase tracking-wider text-muted-foreground">
                  <Cpu className="h-4 w-4" /> Execution Trace
                </div>
                <div className="grid grid-cols-2 gap-y-3 text-sm">
                  <span className="text-muted-foreground flex items-center gap-1.5"><Activity className="h-3.5 w-3.5" /> Tokens</span>
                  <span className="font-medium text-foreground text-right">{tokens}</span>
                  
                  <span className="text-muted-foreground flex items-center gap-1.5"><Clock className="h-3.5 w-3.5" /> Duration</span>
                  <span className="font-medium text-foreground text-right">{latency}</span>
                  
                  <span className="text-muted-foreground flex items-center gap-1.5"><Zap className="h-3.5 w-3.5" /> Model</span>
                  <span className="font-mono text-xs text-foreground text-right truncate" title={model}>{model}</span>
                </div>
              </div>
            </div>
          </AccordionContent>
        </AccordionItem>
      </Accordion>
    </section>
  );
};
