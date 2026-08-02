import * as React from 'react';
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from '@/components/ui/accordion';
import type { Report } from '@/features/reports/types/report.types';
import { cn } from '@/lib/utils';

export const ConfidenceAnalysis: React.FC<{ report: Report }> = ({ report }) => {
  let confidenceWidth = "0%";
  let confidenceColor = "bg-muted";
  
  if (report.confidence_score === 'HIGH') { confidenceWidth = "100%"; confidenceColor = "bg-success"; }
  if (report.confidence_score === 'MEDIUM') { confidenceWidth = "66%"; confidenceColor = "bg-primary"; }
  if (report.confidence_score === 'LOW') { confidenceWidth = "33%"; confidenceColor = "bg-warning"; }
  if (report.confidence_score === 'INSUFFICIENT') { confidenceWidth = "10%"; confidenceColor = "bg-destructive"; }

  return (
    <section id="confidence" className="scroll-mt-24">
      <Accordion type="single" collapsible defaultValue="confidence-analysis">
        <AccordionItem value="confidence-analysis">
          <AccordionTrigger className="text-xl font-semibold tracking-tight hover:no-underline">Confidence Analysis</AccordionTrigger>
          <AccordionContent className="pt-4 pb-6">
            {report.confidence_score ? (
              <div className="p-6 rounded-md border border-border/50 bg-card max-w-4xl space-y-6">
                <div className="space-y-2">
                  <div className="flex justify-between text-sm font-medium">
                    <span>Overall Confidence Metric</span>
                    <span className="uppercase">{report.confidence_score}</span>
                  </div>
                  <div className="h-2 w-full bg-muted/30 rounded-full overflow-hidden">
                    <div className={cn("h-full transition-all duration-1000", confidenceColor)} style={{ width: confidenceWidth }} />
                  </div>
                </div>
                
                <div className="pt-4 border-t border-border/20">
                  <h4 className="text-sm font-medium mb-2">Evidence Coverage & Uncertainty</h4>
                  <p className="text-sm text-foreground/80 leading-relaxed">
                    {report.confidence_explanation || "No additional confidence analysis provided."}
                  </p>
                </div>
              </div>
            ) : (
              <div className="p-6 rounded-md border border-dashed border-border/50 bg-muted/10 max-w-4xl">
                <p className="text-sm font-medium">No confidence analysis available.</p>
                <p className="text-xs text-muted-foreground mt-1">Generate an AI report to view uncertainty and coverage metrics.</p>
              </div>
            )}
          </AccordionContent>
        </AccordionItem>
      </Accordion>
    </section>
  );
};
