import * as React from 'react';
import type { ReportVersionSummary } from '../../types/report.types';
import { ReportStatus, ReportVersionBadge } from '@/components/report';
import { formatDate } from '@/utils';

export const ReportVersions: React.FC<{ versions: ReportVersionSummary[] }> = ({ versions }) => {
  return (
    <section id="versions" className="scroll-mt-24 space-y-4">
      <div className="flex justify-between items-center max-w-4xl">
        <h2 className="text-2xl font-semibold tracking-tight">Version History</h2>
        {/* Placeholder for future diff UI */}
        <button className="text-sm font-medium text-muted-foreground hover:text-foreground hover:underline cursor-not-allowed opacity-50" disabled title="Comparison will be available once version history is implemented.">
          Compare Versions
        </button>
      </div>
      
      {versions && versions.length > 0 ? (
        <div className="rounded-md border border-border/50 bg-card overflow-hidden max-w-4xl">
          <table className="w-full text-sm text-left">
            <thead className="bg-muted/50 text-muted-foreground">
              <tr>
                <th className="px-4 py-3 font-medium">Version</th>
                <th className="px-4 py-3 font-medium">Status</th>
                <th className="px-4 py-3 font-medium">Confidence</th>
                <th className="px-4 py-3 font-medium">Generated At</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border/50">
              {versions.map(v => (
                <tr key={v.id} className="hover:bg-muted/20">
                  <td className="px-4 py-3">
                    <ReportVersionBadge version={v.version} isCurrent={v.is_current} />
                  </td>
                  <td className="px-4 py-3"><ReportStatus status={v.status} showIcon={false} /></td>
                  <td className="px-4 py-3">{v.confidence_score || 'N/A'}</td>
                  <td className="px-4 py-3 text-muted-foreground">{formatDate(v.generated_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="p-6 rounded-md border border-dashed border-border/50 bg-muted/10 max-w-4xl">
          <p className="text-sm font-medium">No version history available.</p>
        </div>
      )}
    </section>
  );
};
