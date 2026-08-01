import { useParams, Link } from "react-router-dom";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ArrowLeft, Brain, TrendingUp, History, Target } from "lucide-react";

export function EmployeeProfile() {
  const { id } = useParams();

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Link to="/employees">
          <Button variant="ghost" size="icon" className="h-8 w-8 rounded-full">
            <ArrowLeft className="h-4 w-4" />
          </Button>
        </Link>
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Sarah Jenkins</h2>
          <p className="text-muted-foreground mt-1 flex items-center gap-2">
            Senior Frontend Engineer <Badge variant="outline">Engineering</Badge>
          </p>
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        <Card className="md:col-span-1">
          <CardHeader>
            <CardTitle>Profile Snapshot</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex justify-between items-center pb-2 border-b border-border">
              <span className="text-muted-foreground text-sm">Manager</span>
              <span className="font-medium">David Kim</span>
            </div>
            <div className="flex justify-between items-center pb-2 border-b border-border">
              <span className="text-muted-foreground text-sm">Current Score</span>
              <span className="font-bold text-verified-teal">9.2/10</span>
            </div>
            <div className="flex justify-between items-center pb-2 border-b border-border">
              <span className="text-muted-foreground text-sm">Promotion Readiness</span>
              <Badge variant="success">High</Badge>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-muted-foreground text-sm">Flight Risk</span>
              <Badge variant="outline">Low</Badge>
            </div>
          </CardContent>
        </Card>

        <Card className="md:col-span-2">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <div>
              <CardTitle>AI Performance Insights</CardTitle>
              <CardDescription>Synthesized from 360° feedback and metrics.</CardDescription>
            </div>
            <Brain className="h-5 w-5 text-brand-blue" />
          </CardHeader>
          <CardContent>
            <div className="space-y-4 mt-4">
              <div className="p-4 bg-muted/30 rounded-lg border border-border">
                <h4 className="font-medium text-sm flex items-center mb-2">
                  <TrendingUp className="mr-2 h-4 w-4 text-verified-teal" /> 
                  Key Strengths
                </h4>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  Consistently delivers high-quality code. Peer reviews frequently mention her exceptional mentoring skills and ability to unblock junior developers. Strong architectural vision demonstrated in the recent Q3 migration project.
                </p>
              </div>
              <div className="p-4 bg-muted/30 rounded-lg border border-border">
                <h4 className="font-medium text-sm flex items-center mb-2">
                  <Target className="mr-2 h-4 w-4 text-brand-blue" /> 
                  Areas for Growth
                </h4>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  Could benefit from taking more proactive leadership in cross-functional sprint planning. Occasionally over-engineers solutions for simple feature requests.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="md:col-span-3">
          <CardHeader>
            <CardTitle className="flex items-center">
              <History className="mr-2 h-5 w-5" />
              Review History
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { cycle: "Q3 2026 Review", score: "9.2", status: "Completed", date: "Oct 15, 2026" },
                { cycle: "Q2 2026 Review", score: "8.9", status: "Completed", date: "Jul 10, 2026" },
                { cycle: "Q1 2026 Review", score: "8.5", status: "Completed", date: "Apr 12, 2026" },
              ].map((review, i) => (
                <div key={i} className="flex items-center justify-between p-4 border border-border rounded-lg hover:bg-muted/50 transition-colors">
                  <div>
                    <p className="font-medium">{review.cycle}</p>
                    <p className="text-sm text-muted-foreground">{review.date}</p>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="text-right">
                      <p className="text-sm text-muted-foreground">Score</p>
                      <p className="font-bold">{review.score}</p>
                    </div>
                    <Badge variant="success">{review.status}</Badge>
                    <Button variant="outline" size="sm">View Details</Button>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
