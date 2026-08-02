import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Plus, PlayCircle, CheckCircle2, Clock } from "lucide-react";

const cycles = [
  { id: "CYC-26Q3", name: "Q3 2026 Engineering Review", status: "Active", progress: 68, deadline: "Oct 30, 2026" },
  { id: "CYC-26Q3-S", name: "Q3 2026 Sales & Marketing", status: "Active", progress: 42, deadline: "Nov 15, 2026" },
  { id: "CYC-26Q2", name: "Q2 2026 Company-Wide", status: "Completed", progress: 100, deadline: "Jul 15, 2026" },
  { id: "CYC-26Q4", name: "Q4 2026 Annual Review", status: "Draft", progress: 0, deadline: "Jan 15, 2027" },
];

export function ReviewCycles() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Review Cycles</h2>
          <p className="text-muted-foreground mt-1">Manage performance review workflows and timelines.</p>
        </div>
        <Button><Plus className="mr-2 h-4 w-4" /> Create Cycle</Button>
      </div>

      <div className="grid gap-6 md:grid-cols-3 mb-6">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm text-muted-foreground font-medium">Active Cycles</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">2</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm text-muted-foreground font-medium">Pending Approvals</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">14</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm text-muted-foreground font-medium">Avg Completion Time</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">14.2 <span className="text-sm font-normal text-muted-foreground">days</span></div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>All Cycles</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Cycle Name</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Progress</TableHead>
                <TableHead>Deadline</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {cycles.map((cycle) => (
                <TableRow key={cycle.id}>
                  <TableCell className="font-medium">{cycle.name}</TableCell>
                  <TableCell>
                    <Badge variant={
                      cycle.status === 'Active' ? 'default' : 
                      cycle.status === 'Completed' ? 'success' : 'secondary'
                    }>
                      {cycle.status === 'Active' && <PlayCircle className="mr-1 h-3 w-3 inline" />}
                      {cycle.status === 'Completed' && <CheckCircle2 className="mr-1 h-3 w-3 inline" />}
                      {cycle.status === 'Draft' && <Clock className="mr-1 h-3 w-3 inline" />}
                      {cycle.status}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <div className="w-full bg-muted rounded-full h-2 max-w-[100px]">
                        <div 
                          className={`h-2 rounded-full ${cycle.status === 'Completed' ? 'bg-success' : 'bg-primary'}`} 
                          style={{ width: `${cycle.progress}%` }}
                        ></div>
                      </div>
                      <span className="text-xs text-muted-foreground">{cycle.progress}%</span>
                    </div>
                  </TableCell>
                  <TableCell className="text-muted-foreground">{cycle.deadline}</TableCell>
                  <TableCell className="text-right">
                    <Button variant="ghost" size="sm">Manage</Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}

