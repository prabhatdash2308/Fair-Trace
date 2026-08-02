import * as React from 'react';
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from '@/components/ui/accordion';

export const LimitationsPanel: React.FC = () => {
  return (
    <section id="limitations" className="scroll-mt-24">
      <Accordion type="single" collapsible defaultValue="limitations">
        <AccordionItem value="limitations">
          <AccordionTrigger className="text-xl font-semibold tracking-tight hover:no-underline">AI Limitations</AccordionTrigger>
          <AccordionContent className="pt-4 pb-6">
            <div className="p-6 rounded-md border border-dashed border-border/50 bg-muted/10 max-w-4xl">
              <p className="text-sm font-medium">No limitations reported.</p>
              <p className="text-xs text-muted-foreground mt-1">If the AI detects blindspots in the evaluation, they will appear here.</p>
            </div>
          </AccordionContent>
        </AccordionItem>
      </Accordion>
    </section>
  );
};
