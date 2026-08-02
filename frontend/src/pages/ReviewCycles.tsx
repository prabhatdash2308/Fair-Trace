import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { PageHeader } from "@/components/shared/PageHeader";
import { MetricCard } from "@/components/shared/MetricCard";
import { Plus, PlayCircle, CheckCircle2, Clock, Target, Users, Timer, ArrowRight } from "lucide-react";
import { cn } from "@/lib/utils";

const cycles = [
  { id: "CYC-26Q3",   name: "Q3 2026 Engineering Review",  status: "Active",    progress: 68,  deadline: "Oct 30, 2026" },
  { id: "CYC-26Q3-S", name: "Q3 2026 Sales & Marketing",   status: "Active",    progress: 42,  deadline: "Nov 15, 2026" },
  { id: "CYC-26Q2",   name: "Q2 2026 Company-Wide Review", status: "Completed", progress: 100, deadline: "Jul 15, 2026" },
  { id: "CYC-26Q4",   name: "Q4 2026 Annual Review",       status: "Draft",     progress: 0,   deadline: "Jan 15, 2027" },
];

const STATUS_CONFIG = {
  Active:    { variant: 'default'     as const, icon: PlayCircle,   label: 'Active'    },
  Completed: { variant: 'success'     as const, icon: CheckCircle2, label: 'Completed' },
  Draft:     { variant: 'secondary'   as const, icon: Clock,        label: 'Draft'     },
};

function ProgressBar({ progress, status }: { progress: number; status: string }) {
  const color = status === 'Completed' ? 'bg-success' : status === 'Active' ? 'bg-primary' : 'bg-muted-foreground/30';
  return (
    <div className="flex items-center gap-2.5">
      <div className="flex-1 max-w-[96px] h-1.5 rounded-full bg-muted overflow-hidden">
        <div
          className={cn('h-full rounded-full transition-all duration-500', color)}
          style={{ width: `${progress}%` }}
        />
      </div>
      <span className="text-caption tabular-nums text-muted-foreground w-9 text-right">
        {progress}%
      </span>
    </div>
  );
}

export function ReviewCycles() {
  return (
    <div className="space-y-0">
      <PageHeader
        title="Review Cycles"
        subtitle="Manage performance review workflows and timelines."
        actions={
          <Button size="sm">
            <Plus className="h-4 w-4" />
            Create Cycle
          </Button>
        }
      />

      {/* KPI row */}
      <div className="grid gap-4 sm:grid-cols-3 mb-8">
        <MetricCard
          title="Active Cycles"
          value="2"
          description="In progress"
          icon={Target}
          variant="default"
          trend={{ direction: 'up', value: 1, label: 'vs last quarter' }}
        />
        <MetricCard
          title="Pending Approvals"
          value="14"
          description="Awaiting review"
          icon={Users}
          variant="warning"
        />
        <MetricCard
          title="Avg Completion"
          value="14.2d"
          description="Per review cycle"
          icon={Timer}
          variant="success"
          trend={{ direction: 'down', value: 2.1, label: 'faster' }}
        />
      </div>

      {/* Cycles table */}
      <Card>
        <CardHeader className="border-b border-border py-4">
          <div className="flex items-center justify-between">
            <CardTitle>All Cycles</CardTitle>
            <Button variant="ghost" size="sm" className="gap-1 text-muted-foreground">
              View history
              <ArrowRight className="h-3.5 w-3.5" />
            </Button>
          </div>
        </CardHeader>
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Cycle Name</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="w-[180px]">Progress</TableHead>
                <TableHead>Deadline</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {cycles.map((cycle) => {
                const cfg = STATUS_CONFIG[cycle.status as keyof typeof STATUS_CONFIG];
                return (
                  <TableRow key={cycle.id}>
                    <TableCell>
                      <div>
                        <p className="text-body font-medium text-foreground">{cycle.name}</p>
                        <p className="text-caption text-muted-foreground font-mono">{cycle.id}</p>
                      </div>
                    </TableCell>
                    <TableCell>
                      <Badge variant={cfg.variant} className="gap-1">
                        <cfg.icon className="h-3 w-3" aria-hidden="true" />
                        {cfg.label}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <ProgressBar progress={cycle.progress} status={cycle.status} />
                    </TableCell>
                    <TableCell className="text-body text-muted-foreground">
                      {cycle.deadline}
                    </TableCell>
                    <TableCell className="text-right">
                      <Button variant="outline" size="sm">
                        Manage
                      </Button>
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
