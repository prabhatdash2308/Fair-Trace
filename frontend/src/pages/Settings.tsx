import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export function Settings() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">Platform Settings</h2>
        <p className="text-muted-foreground mt-1">Configure workspace, security, and AI parameters.</p>
      </div>

      <div className="grid gap-6 md:grid-cols-4">
        <div className="md:col-span-1 space-y-1 flex flex-col">
          <Button variant="secondary" className="justify-start">Workspace</Button>
          <Button variant="ghost" className="justify-start">Security & SSO</Button>
          <Button variant="ghost" className="justify-start">Roles & Permissions</Button>
          <Button variant="ghost" className="justify-start">Notifications</Button>
          <Button variant="ghost" className="justify-start">Integrations</Button>
        </div>
        
        <div className="md:col-span-3 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Workspace Profile</CardTitle>
              <CardDescription>Manage your organization's core details.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">Company Name</label>
                <Input defaultValue="Acme Corp Enterprise" />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Primary Domain</label>
                <Input defaultValue="acmecorp.com" />
              </div>
              <Button>Save Changes</Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>AI Configuration</CardTitle>
              <CardDescription>Adjust how the ReviewGuard AI analyzes performance data.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium flex items-center justify-between">
                  <span>Bias Detection Sensitivity</span>
                  <span className="text-primary">High</span>
                </label>
                <input type="range" className="w-full accent-primary" min="1" max="3" defaultValue="3" />
              </div>
              <div className="pt-4">
                <Button variant="outline">Reset to Defaults</Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}

