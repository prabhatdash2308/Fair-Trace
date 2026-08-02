import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { PageHeader } from "@/components/shared/PageHeader";
import { Download, BarChart3, Scale, FileSpreadsheet, FileText, Clock, ArrowRight } from "lucide-react";
import { cn } from "@/lib/utils";

interface ReportCardProps {
  icon: React.ElementType;
  iconColor: string;
  iconBg: string;
  title: string;
  description: string;
  lastGenerated?: string;
  status?: 'ready' | 'processing' | 'unavailable';
  onDownload?: () => void;
  onPreview?: () => void;
}

function ReportCard({
  icon: Icon,
  iconColor,
  iconBg,
  title,
  description,
  lastGenerated,
  status = 'ready',
  onDownload,
  onPreview,
}: ReportCardProps) {
  return (
    <Card className="flex flex-col hover:shadow-md transition-shadow duration-[160ms]">
      <CardHeader className="pb-3">
        <div className="flex items-start gap-4">
          {/* Icon container */}
          <div className={cn(
            'flex items-center justify-center h-10 w-10 rounded-lg border shrink-0',
            iconBg,
          )}>
            <Icon className={cn('h-5 w-5', iconColor)} aria-hidden="true" />
          </div>
          <div className="min-w-0 flex-1">
            <div className="flex items-center gap-2 mb-0.5">
              <CardTitle className="truncate">{title}</CardTitle>
              {status === 'ready' && (
                <Badge variant="success" className="shrink-0">Ready</Badge>
              )}
              {status === 'processing' && (
                <Badge variant="warning" className="shrink-0">Processing</Badge>
              )}
              {status === 'unavailable' && (
                <Badge variant="secondary" className="shrink-0">Unavailable</Badge>
              )}
            </div>
            <CardDescription className="leading-relaxed">{description}</CardDescription>
          </div>
        </div>
      </CardHeader>

      {lastGenerated && (
        <CardContent className="py-0 pb-3">
          <div className="flex items-center gap-1.5 text-caption text-muted-foreground">
            <Clock className="h-3 w-3" aria-hidden="true" />
            Last generated: {lastGenerated}
          </div>
        </CardContent>
      )}

      <CardFooter className="mt-auto pt-4 border-t border-border/60 gap-2">
        <Button
          variant="default"
          size="sm"
          className="flex-1"
          onClick={onDownload}
          disabled={status !== 'ready'}
        >
          <Download className="h-4 w-4" />
          Download PDF
        </Button>
        <Button
          variant="ghost"
          size="icon-sm"
          onClick={onPreview}
          disabled={status !== 'ready'}
          aria-label={`Preview ${title}`}
        >
          <ArrowRight className="h-4 w-4" />
        </Button>
      </CardFooter>
    </Card>
  );
}

export function Reports() {
  return (
    <div className="space-y-0">
      <PageHeader
        title="Reports & Exports"
        subtitle="Generate, download, and share organizational performance documents."
      />

      <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        <ReportCard
          icon={BarChart3}
          iconColor="text-primary"
          iconBg="bg-primary/10 border-primary/20"
          title="Department Comparisons"
          description="Performance score distribution and trend analysis across all departments for the current cycle."
          lastGenerated="Jul 28, 2026"
          status="ready"
          onDownload={() => {}}
          onPreview={() => {}}
        />

        <ReportCard
          icon={Scale}
          iconColor="text-warning"
          iconBg="bg-warning/10 border-warning/20"
          title="Bias & Fairness Audit"
          description="AI-generated analysis of language bias, demographic fairness, and calibration consistency across reviews."
          lastGenerated="Jul 25, 2026"
          status="ready"
          onDownload={() => {}}
          onPreview={() => {}}
        />

        <ReportCard
          icon={FileSpreadsheet}
          iconColor="text-success"
          iconBg="bg-success/10 border-success/20"
          title="Raw Data Export"
          description="Full dataset export of all employee performance data for external BI tools and compliance records."
          lastGenerated="Aug 1, 2026"
          status="ready"
          onDownload={() => {}}
          onPreview={() => {}}
        />

        <ReportCard
          icon={FileText}
          iconColor="text-info"
          iconBg="bg-info/10 border-info/20"
          title="Executive Summary"
          description="High-level performance overview for leadership — KPIs, trends, outliers, and recommendations."
          status="processing"
          onDownload={() => {}}
          onPreview={() => {}}
        />

        <ReportCard
          icon={BarChart3}
          iconColor="text-muted-foreground"
          iconBg="bg-muted border-border"
          title="Individual Reports"
          description="Per-employee performance review reports with AI-generated insights and evidence citations."
          status="unavailable"
        />
      </div>
    </div>
  );
}
