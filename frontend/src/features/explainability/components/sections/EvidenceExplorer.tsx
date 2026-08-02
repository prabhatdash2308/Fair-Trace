import * as React from 'react';
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from '@/components/ui/accordion';
import type { Report } from '@/features/reports/types/report.types';
import { CitationCard } from '@/components/explainability';

export const EvidenceExplorer: React.FC<{ report: Report }> = ({ report }) => {
  const allCitations = report.claims?.flatMap(c => c.citations) || [];

  return (
    <section id="evidence" className="scroll-mt-24">
      <Accordion type="single" collapsible defaultValue="evidence-explorer">
        <AccordionItem value="evidence-explorer">
          <AccordionTrigger className="text-xl font-semibold tracking-tight hover:no-underline">Raw Evidence</AccordionTrigger>
          <AccordionContent className="pt-4 pb-6">
            {allCitations.length > 0 ? (
              <div className="space-y-4 max-w-4xl">
                {allCitations.map((cit, idx) => (
                  <CitationCard key={cit.id || idx} citation={cit} />
                ))}
              </div>
            ) : (
              <div className="p-6 rounded-md border border-dashed border-border/50 bg-muted/10 max-w-4xl">
                <p className="text-sm font-medium">No supporting evidence available.</p>
                <p className="text-xs text-muted-foreground mt-1">AI was unable to extract concrete citations for this evaluation.</p>
              </div>
            )}
          </AccordionContent>
        </AccordionItem>
      </Accordion>
    </section>
  );
};
