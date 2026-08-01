import { useState } from "react";
import { Link } from "react-router-dom";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Search, Filter, MoreHorizontal, Download } from "lucide-react";

const employeesData = [
  { id: "EMP-1021", name: "Sarah Jenkins", role: "Senior Frontend Engineer", dept: "Engineering", manager: "David Kim", score: 9.2, risk: "Low", status: "Active" },
  { id: "EMP-1022", name: "Marcus Chen", role: "Product Manager", dept: "Product", manager: "Sarah Jenkins", score: 8.7, risk: "Low", status: "Active" },
  { id: "EMP-1023", name: "Aisha Patel", role: "UX Designer", dept: "Design", manager: "Elena Rodriguez", score: 9.5, risk: "High", status: "Active" },
  { id: "EMP-1024", name: "Tom Wilson", role: "Backend Engineer", dept: "Engineering", manager: "David Kim", score: 7.8, risk: "Medium", status: "Active" },
  { id: "EMP-1025", name: "Jessica Lee", role: "Marketing Director", dept: "Marketing", manager: "Michael Chang", score: 8.9, risk: "Low", status: "On Leave" },
  { id: "EMP-1026", name: "Ryan Martinez", role: "Sales Executive", dept: "Sales", manager: "Jessica Lee", score: 9.1, risk: "High", status: "Active" },
];

export function Employees() {
  const [searchTerm, setSearchTerm] = useState("");

  const filteredEmployees = employeesData.filter(emp => 
    emp.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
    emp.role.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Employee Directory</h2>
          <p className="text-muted-foreground mt-1">Manage and review workforce performance data.</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline"><Download className="mr-2 h-4 w-4" /> Export CSV</Button>
          <Button>Add Employee</Button>
        </div>
      </div>

      <Card>
        <CardHeader className="py-4 border-b border-border">
          <div className="flex flex-col sm:flex-row justify-between gap-4">
            <div className="relative max-w-sm w-full">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input 
                placeholder="Search employees..." 
                className="pl-9" 
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
            <div className="flex gap-2">
              <Button variant="outline" size="sm" className="h-10"><Filter className="mr-2 h-4 w-4" /> Filter</Button>
            </div>
          </div>
        </CardHeader>
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name & Role</TableHead>
                <TableHead>Department</TableHead>
                <TableHead>Manager</TableHead>
                <TableHead className="text-right">Perf. Score</TableHead>
                <TableHead className="text-center">Flight Risk</TableHead>
                <TableHead className="text-center">Status</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredEmployees.map((emp) => (
                <TableRow key={emp.id} className="hover:bg-muted/50 transition-colors">
                  <TableCell>
                    <Link to={`/employees/${emp.id}`} className="block">
                      <div className="font-medium text-foreground hover:text-brand-blue transition-colors">{emp.name}</div>
                      <div className="text-xs text-muted-foreground">{emp.role}</div>
                    </Link>
                  </TableCell>
                  <TableCell>{emp.dept}</TableCell>
                  <TableCell>{emp.manager}</TableCell>
                  <TableCell className="text-right font-medium">
                    <span className={emp.score >= 9 ? "text-verified-teal" : emp.score < 8 ? "text-warning-orange" : ""}>
                      {emp.score}
                    </span>
                  </TableCell>
                  <TableCell className="text-center">
                    <Badge variant={emp.risk === 'High' ? 'destructive' : emp.risk === 'Medium' ? 'warning' : 'outline'}>
                      {emp.risk}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-center">
                    <Badge variant={emp.status === 'Active' ? 'success' : 'secondary'}>
                      {emp.status}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right">
                    <Button variant="ghost" size="icon">
                      <MoreHorizontal className="h-4 w-4" />
                    </Button>
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
