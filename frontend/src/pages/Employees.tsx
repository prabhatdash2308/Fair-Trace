import { useState } from "react";
import { Link } from "react-router-dom";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { PageHeader } from "@/components/shared/PageHeader";
import { EmptyState } from "@/components/shared/EmptyState";
import { Search, Filter, Download, Plus, Users } from "lucide-react";
import { cn } from "@/lib/utils";

const employeesData = [
  { id: "EMP-1021", name: "Sarah Jenkins",  role: "Senior Frontend Engineer", dept: "Engineering", manager: "David Kim",       score: 9.2, risk: "Low",    status: "Active"   },
  { id: "EMP-1022", name: "Marcus Chen",    role: "Product Manager",          dept: "Product",     manager: "Sarah Jenkins",  score: 8.7, risk: "Low",    status: "Active"   },
  { id: "EMP-1023", name: "Aisha Patel",    role: "UX Designer",              dept: "Design",      manager: "Elena Rodriguez",score: 9.5, risk: "High",   status: "Active"   },
  { id: "EMP-1024", name: "Tom Wilson",     role: "Backend Engineer",         dept: "Engineering", manager: "David Kim",       score: 7.8, risk: "Medium", status: "Active"   },
  { id: "EMP-1025", name: "Jessica Lee",    role: "Marketing Director",       dept: "Marketing",   manager: "Michael Chang",   score: 8.9, risk: "Low",    status: "On Leave" },
  { id: "EMP-1026", name: "Ryan Martinez",  role: "Sales Executive",          dept: "Sales",       manager: "Jessica Lee",     score: 9.1, risk: "High",   status: "Active"   },
];

// Department → subtle color chip
const DEPT_COLORS: Record<string, string> = {
  Engineering: "bg-info/10 text-info border-info/20",
  Product:     "bg-primary/10 text-primary border-primary/20",
  Design:      "bg-warning/10 text-warning border-warning/20",
  Marketing:   "bg-success/10 text-success border-success/20",
  Sales:       "bg-danger/10 text-danger border-danger/20",
};

// Generate initials + stable color from name
function getInitials(name: string) {
  return name.split(' ').map(n => n[0]).slice(0, 2).join('').toUpperCase();
}
const AVATAR_COLORS = [
  'bg-primary/15 text-primary border-primary/25',
  'bg-success/15 text-success border-success/25',
  'bg-warning/15 text-warning border-warning/25',
  'bg-info/15 text-info border-info/25',
  'bg-danger/15 text-danger border-danger/25',
];
function getAvatarColor(name: string) {
  const hash = name.split('').reduce((a, c) => a + c.charCodeAt(0), 0);
  return AVATAR_COLORS[hash % AVATAR_COLORS.length];
}

// Score mini-bar
function ScoreBar({ score }: { score: number }) {
  const pct = (score / 10) * 100;
  const color = score >= 9 ? 'bg-success' : score >= 8 ? 'bg-primary' : 'bg-warning';
  return (
    <div className="flex items-center gap-2">
      <div className="w-16 h-1.5 rounded-full bg-muted overflow-hidden">
        <div className={cn('h-full rounded-full', color)} style={{ width: `${pct}%` }} />
      </div>
      <span className={cn(
        'text-caption tabular-nums font-medium',
        score >= 9 ? 'text-success' : score < 8 ? 'text-warning' : 'text-foreground'
      )}>
        {score}
      </span>
    </div>
  );
}

export function Employees() {
  const [searchTerm, setSearchTerm] = useState("");

  const filtered = employeesData.filter(emp =>
    emp.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    emp.role.toLowerCase().includes(searchTerm.toLowerCase()) ||
    emp.dept.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-0">
      <PageHeader
        title="Employee Directory"
        subtitle="Browse and manage workforce performance data."
        actions={
          <>
            <Button variant="outline" size="sm">
              <Download className="h-4 w-4" />
              Export CSV
            </Button>
            <Button size="sm">
              <Plus className="h-4 w-4" />
              Add Employee
            </Button>
          </>
        }
      />

      <Card>
        {/* Table toolbar */}
        <CardHeader className="py-3 border-b border-border">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
            <div className="relative w-full sm:max-w-64">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground" aria-hidden="true" />
              <Input
                id="employee-search"
                placeholder="Search employees…"
                className="pl-8"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                aria-label="Search employees"
              />
            </div>
            <div className="flex items-center gap-2 shrink-0">
              <Button variant="outline" size="sm">
                <Filter className="h-4 w-4" />
                Filter
              </Button>
              <span className="text-caption text-muted-foreground">
                {filtered.length} of {employeesData.length} employees
              </span>
            </div>
          </div>
        </CardHeader>

        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-[240px]">Employee</TableHead>
                <TableHead>Department</TableHead>
                <TableHead className="hidden md:table-cell">Manager</TableHead>
                <TableHead>Performance</TableHead>
                <TableHead className="text-center">Flight Risk</TableHead>
                <TableHead className="text-center">Status</TableHead>
                <TableHead className="w-12" />
              </TableRow>
            </TableHeader>
            <TableBody>
              {filtered.length === 0 ? (
                <TableRow>
                  <td colSpan={7}>
                    <EmptyState
                      icon={Users}
                      title="No employees found"
                      description={`No results for "${searchTerm}". Try adjusting your search.`}
                      action={{ label: 'Clear search', onClick: () => setSearchTerm('') }}
                      size="sm"
                    />
                  </td>
                </TableRow>
              ) : (
                filtered.map((emp) => (
                  <TableRow key={emp.id}>
                    {/* Employee cell — avatar + name + role */}
                    <TableCell>
                      <Link to={`/employees/${emp.id}`} className="flex items-center gap-3 group">
                        <div className={cn(
                          'h-8 w-8 rounded-full border flex items-center justify-center',
                          'text-[11px] font-semibold shrink-0 select-none',
                          getAvatarColor(emp.name),
                        )}>
                          {getInitials(emp.name)}
                        </div>
                        <div className="min-w-0">
                          <p className="text-body font-medium text-foreground group-hover:text-primary transition-colors duration-[120ms] truncate">
                            {emp.name}
                          </p>
                          <p className="text-caption text-muted-foreground truncate">{emp.role}</p>
                        </div>
                      </Link>
                    </TableCell>

                    {/* Department */}
                    <TableCell>
                      <span className={cn(
                        'inline-flex items-center px-2 py-0.5 rounded-md border text-[11px] font-medium',
                        DEPT_COLORS[emp.dept] ?? 'bg-muted text-muted-foreground border-border',
                      )}>
                        {emp.dept}
                      </span>
                    </TableCell>

                    {/* Manager */}
                    <TableCell className="hidden md:table-cell text-muted-foreground">
                      {emp.manager}
                    </TableCell>

                    {/* Performance score with mini bar */}
                    <TableCell>
                      <ScoreBar score={emp.score} />
                    </TableCell>

                    {/* Flight Risk */}
                    <TableCell className="text-center">
                      <Badge variant={
                        emp.risk === 'High'   ? 'destructive' :
                        emp.risk === 'Medium' ? 'warning'     : 'success'
                      }>
                        {emp.risk}
                      </Badge>
                    </TableCell>

                    {/* Status */}
                    <TableCell className="text-center">
                      <Badge variant={emp.status === 'Active' ? 'success' : 'secondary'}>
                        {emp.status}
                      </Badge>
                    </TableCell>

                    {/* Actions */}
                    <TableCell className="text-right">
                      <Button variant="ghost" size="icon-sm" aria-label={`Options for ${emp.name}`}>
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
                          <circle cx="8" cy="3" r="1.2" />
                          <circle cx="8" cy="8" r="1.2" />
                          <circle cx="8" cy="13" r="1.2" />
                        </svg>
                      </Button>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
