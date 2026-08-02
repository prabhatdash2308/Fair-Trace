import * as React from 'react';
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from '@/components/ui/accordion';
import type { Report } from '@/features/reports/types/report.types';
import { AlertCircle } from 'lucide-react';

export const BiasAnalysis: React.FC<{ report: Report }> = ({ report }) => {
  const hasBias = report.bias_flags && report.bias_flags.length > 0;

  return (
    <section id="bias" className="scroll-mt-24">
      <Accordion type="single" collapsible defaultValue="bias-analysis">
        <AccordionItem value="bias-analysis">
          <AccordionTrigger className="text-xl font-semibold tracking-tight hover:no-underline">Bias Analysis</AccordionTrigger>
          <AccordionContent className="pt-4 pb-6">
            {hasBias ? (
              <div className="space-y-4 max-w-4xl">
                {report.bias_flags.map((bias) => (
                  <div key={bias.id} className="p-4 rounded-md border border-warning/30 bg-warning/5 flex gap-4">
                    <AlertCircle className="h-5 w-5 text-warning-foreground shrink-0 mt-0.5" />
                    <div>
                      <h4 className="text-sm font-medium text-warning-foreground mb-1">
                        {bias.bias_type} BIAS DETECTED
                      </h4>
                      <p className="text-sm text-foreground/80 mb-2">{bias.detection_reasoning}</p>
                      {bias.affected_text && (
                        <div className="text-xs p-2 bg-background/50 rounded border border-border/30 mb-2 italic text-foreground/70">
                          "{bias.affected_text}"
                        </div>
                      )}
                      <p className="text-xs font-medium text-muted-foreground mt-2">Recommended Action: <span className="text-foreground/90">{bias.recommended_action}</span></p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="p-6 rounded-md border border-dashed border-border/50 bg-muted/10 max-w-4xl">
                <p className="text-sm font-medium">No bias detected in this analysis.</p>
                <p className="text-xs text-muted-foreground mt-1">The retrieved evidence did not trigger any cognitive bias thresholds.</p>
              </div>
            )}
          </AccordionContent>
        </AccordionItem>
      </Accordion>
    </section>
  );
};
