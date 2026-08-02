import * as React from 'react';
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from '@/components/ui/accordion';
import type { Report } from '@/features/reports/types/report.types';
import { Timeline, type TimelineEvent } from '@/components/timeline';
import { FileSearch, BrainCircuit, Activity, FileText } from 'lucide-react';
import { formatDate } from '@/utils';

export const ReasoningChain: React.FC<{ report: Report }> = ({ report }) => {
  const events: TimelineEvent[] = [
    { id: '1', title: 'Evidence Retrieval', date: formatDate(report.generated_at), icon: FileSearch, isActive: false, description: 'Extracted semantic chunks from performance inputs.' },
    { id: '2', title: 'Bias Detection', date: formatDate(report.generated_at), icon: Activity, isActive: false, description: 'Analyzed retrieved chunks for cognitive biases (e.g. Recency, Halo).' },
    { id: '3', title: 'Performance Analysis', date: formatDate(report.generated_at), icon: BrainCircuit, isActive: false, description: 'Evaluated core competencies against criteria.' },
    { id: '4', title: 'Explainability & Report Generation', date: formatDate(report.generated_at), icon: FileText, isActive: true, description: 'Synthesized findings into traceable claims.' }
  ];

  return (
    <section id="reasoning" className="scroll-mt-24">
      <Accordion type="single" collapsible defaultValue="reasoning-chain">
        <AccordionItem value="reasoning-chain">
          <AccordionTrigger className="text-xl font-semibold tracking-tight hover:no-underline">Reasoning Chain</AccordionTrigger>
          <AccordionContent className="pt-4 pb-6">
            <div className="p-6 rounded-lg border border-border/50 bg-card max-w-4xl">
              <Timeline events={events} />
            </div>
          </AccordionContent>
        </AccordionItem>
      </Accordion>
    </section>
  );
};
