import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { BrainCircuit, AlertTriangle, Lightbulb, TrendingDown } from "lucide-react";

export function AIInsights() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">AI Insights</h2>
        <p className="text-muted-foreground mt-1">Predictive analytics and automated organizational intelligence.</p>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        <Card className="md:col-span-2 border-brand-blue/20 bg-brand-blue/5">
          <CardHeader>
            <CardTitle className="flex items-center text-brand-blue">
              <BrainCircuit className="mr-2 h-5 w-5" />
              Primary Recommendation
            </CardTitle>
            <CardDescription>Based on analysis of 12,482 performance reviews in Q3.</CardDescription>
          </CardHeader>
          <CardContent>
            <h3 className="text-lg font-semibold mb-2">Standardize technical evaluation criteria across Engineering</h3>
            <p className="text-muted-foreground leading-relaxed">
              Our natural language models detected a 34% variance in how "technical excellence" is described between the Platform and Product engineering teams. This discrepancy correlates with a higher attrition rate in the Platform team for mid-level engineers. We recommend implementing a unified rubric for technical assessment.
            </p>
            <div className="mt-4 flex gap-3">
              <Badge variant="default">High Impact</Badge>
              <Badge variant="outline">Engineering Dept</Badge>
              <Badge variant="success">94% Confidence</Badge>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <AlertTriangle className="mr-2 h-5 w-5 text-warning-orange" />
              Bias Detection
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="p-3 border border-border rounded-lg">
              <p className="text-sm font-medium mb-1">Gendered Language Flag</p>
              <p className="text-xs text-muted-foreground">Detected in 4% of Sales department reviews. <a href="#" className="text-brand-blue hover:underline">View report</a></p>
            </div>
            <div className="p-3 border border-border rounded-lg">
              <p className="text-sm font-medium mb-1">Recency Bias Warning</p>
              <p className="text-xs text-muted-foreground">High concentration of feedback references from the last 30 days only.</p>
            </div>
          </CardContent>
        </Card>
      </div>

      <h3 className="text-xl font-semibold tracking-tight mt-8 mb-4">Predictive Trends</h3>
      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Lightbulb className="mr-2 h-5 w-5 text-verified-teal" />
              Emerging Leaders
            </CardTitle>
            <CardDescription>Identified based on peer feedback sentiment analysis.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {['Design', 'Product', 'Engineering'].map((dept, i) => (
                <div key={i} className="flex justify-between items-center p-2 hover:bg-muted/50 rounded-md transition-colors">
                  <span className="font-medium">{dept}</span>
                  <span className="text-muted-foreground text-sm">{i + 2} candidates identified</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <TrendingDown className="mr-2 h-5 w-5 text-danger-red" />
              Burnout Indicators
            </CardTitle>
            <CardDescription>Teams showing linguistic markers of high stress.</CardDescription>
          </CardHeader>
          <CardContent>
             <div className="space-y-3">
              {['Customer Support', 'DevOps'].map((dept, i) => (
                <div key={i} className="flex justify-between items-center p-2 border-l-2 border-danger-red bg-danger-red/5 rounded-r-md transition-colors">
                  <span className="font-medium text-danger-red">{dept}</span>
                  <span className="text-muted-foreground text-sm">Action required</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
