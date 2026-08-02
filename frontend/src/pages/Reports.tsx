import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Download, FileText, PieChart, BarChart } from "lucide-react";

export function Reports() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Reports & Exports</h2>
          <p className="text-muted-foreground mt-1">Generate and download organizational performance data.</p>
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <BarChart className="mr-2 h-5 w-5 text-primary" />
              Department Comparisons
            </CardTitle>
            <CardDescription>Performance score distribution across all departments.</CardDescription>
          </CardHeader>
          <CardContent>
             <Button variant="outline" className="w-full justify-start">
               <Download className="mr-2 h-4 w-4" /> Download PDF Report
             </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <PieChart className="mr-2 h-5 w-5 text-warning" />
              Bias & Fairness Audit
            </CardTitle>
            <CardDescription>AI-generated report on language bias in recent cycles.</CardDescription>
          </CardHeader>
          <CardContent>
             <Button variant="outline" className="w-full justify-start">
               <Download className="mr-2 h-4 w-4" /> Download Audit (PDF)
             </Button>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <FileText className="mr-2 h-5 w-5 text-success" />
              Raw Data Export
            </CardTitle>
            <CardDescription>Export all employee performance data for external analysis.</CardDescription>
          </CardHeader>
          <CardContent>
             <Button variant="outline" className="w-full justify-start">
               <Download className="mr-2 h-4 w-4" /> Export CSV (All Data)
             </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

