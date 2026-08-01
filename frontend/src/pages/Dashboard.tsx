import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Users, Target, Activity, Zap, ArrowUpRight, ArrowDownRight } from "lucide-react";

export function Dashboard() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Executive Dashboard</h2>
          <p className="text-muted-foreground mt-1">Company performance overview and AI insights.</p>
        </div>
      </div>

      {/* KPIs */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Active Employees</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">12,482</div>
            <p className="text-xs text-muted-foreground mt-1 flex items-center">
              <ArrowUpRight className="mr-1 h-3 w-3 text-verified-teal" />
              <span className="text-verified-teal font-medium">+2.5%</span> from last month
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Avg Performance Score</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">8.4<span className="text-muted-foreground text-sm font-normal">/10</span></div>
            <p className="text-xs text-muted-foreground mt-1 flex items-center">
              <ArrowUpRight className="mr-1 h-3 w-3 text-verified-teal" />
              <span className="text-verified-teal font-medium">+0.2</span> from last cycle
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Reviews Completed</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">94%</div>
            <div className="w-full bg-muted rounded-full h-2 mt-2">
              <div className="bg-brand-blue h-2 rounded-full" style={{ width: '94%' }}></div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Flight Risk Alert</CardTitle>
            <Zap className="h-4 w-4 text-warning-orange" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">142</div>
            <p className="text-xs text-muted-foreground mt-1 flex items-center">
              <ArrowDownRight className="mr-1 h-3 w-3 text-danger-red" />
              <span className="text-danger-red font-medium">+12</span> high performers
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Main Content Area */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-7">
        <Card className="lg:col-span-4">
          <CardHeader>
            <CardTitle>Performance Distribution</CardTitle>
            <CardDescription>Department comparison over the last 4 review cycles.</CardDescription>
          </CardHeader>
          <CardContent className="h-[300px] flex items-center justify-center border-t border-border mt-4 border-dashed">
             <div className="text-muted-foreground flex flex-col items-center">
               <Activity className="h-8 w-8 mb-2 opacity-50" />
               <p>Interactive Recharts Component</p>
             </div>
          </CardContent>
        </Card>

        <Card className="lg:col-span-3">
          <CardHeader>
            <CardTitle>AI Action Items</CardTitle>
            <CardDescription>Automated recommendations requiring approval.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { title: "Promotion Eligibility", desc: "15 engineers identified as ready for L5 promotion based on peer feedback.", status: "Review" },
                { title: "Bias Detection", desc: "Warning: Potential language bias detected in Marketing department reviews.", status: "Action Req" },
                { title: "Skill Gap Analysis", desc: "Design team lacks advanced Framer Motion skills compared to industry standard.", status: "Insight" }
              ].map((item, i) => (
                <div key={i} className="flex flex-col gap-2 p-3 rounded-lg border border-border hover:bg-muted/50 transition-colors">
                  <div className="flex justify-between items-start">
                    <span className="font-medium text-sm">{item.title}</span>
                    <Badge variant={item.status === 'Review' ? 'default' : item.status === 'Action Req' ? 'warning' : 'outline'}>
                      {item.status}
                    </Badge>
                  </div>
                  <p className="text-xs text-muted-foreground">{item.desc}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
