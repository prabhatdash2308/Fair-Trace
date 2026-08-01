import * as React from 'react';
import type { Report } from '../../types/report.types';
import { AlertCircle } from 'lucide-react';

export const ReportBias: React.FC<{ report: Report }> = ({ report }) => {
  const hasBias = report.bias_flags && report.bias_flags.length > 0;

  return (
    <section id="bias" className="scroll-mt-24 space-y-4">
      <h2 className="text-2xl font-semibold tracking-tight">Bias Analysis</h2>
      
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
                  <div className="text-xs p-2 bg-background/50 rounded border border-border/30 mb-2 italic">
                    "{bias.affected_text}"
                  </div>
                )}
                <p className="text-xs font-medium text-muted-foreground">Action: {bias.recommended_action}</p>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="p-6 rounded-md border border-dashed border-border/50 bg-muted/10 max-w-4xl">
          <p className="text-sm font-medium">No AI bias analysis available or no bias detected.</p>
          <p className="text-xs text-muted-foreground mt-1">Generate an AI report from the Review workspace.</p>
        </div>
      )}
    </section>
  );
};
