import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { PageHeader } from "@/components/shared/PageHeader";
import { cn } from "@/lib/utils";
import {
  Building, ShieldCheck, Users, Bell, Plug,
  ChevronRight, Brain, Save
} from "lucide-react";

const NAV_ITEMS = [
  { id: 'workspace',    label: 'Workspace',         icon: Building },
  { id: 'notifications',label: 'Notifications',      icon: Bell },
  { id: 'ai',           label: 'AI Configuration',   icon: Brain },
] as const;

type SettingsTab = (typeof NAV_ITEMS)[number]['id'];

const BIAS_LABELS: Record<number, string> = {
  1: 'Low',
  2: 'Standard',
  3: 'High',
};

function FormRow({ label, description, children }: { label: string; description?: string; children: React.ReactNode }) {
  return (
    <div className="flex flex-col sm:flex-row sm:items-start gap-4 py-4 border-b border-border/60 last:border-0">
      <div className="sm:w-48 shrink-0">
        <p className="text-body font-medium text-foreground">{label}</p>
        {description && (
          <p className="text-caption text-muted-foreground mt-0.5 leading-relaxed">{description}</p>
        )}
      </div>
      <div className="flex-1 min-w-0">{children}</div>
    </div>
  );
}

function ToggleSwitch({ checked, onChange, id }: { checked: boolean; onChange: (v: boolean) => void; id: string }) {
  return (
    <button
      id={id}
      role="switch"
      aria-checked={checked}
      onClick={() => onChange(!checked)}
      className={cn(
        'relative inline-flex h-5 w-9 items-center rounded-full transition-colors duration-[160ms]',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring/50 focus-visible:ring-offset-2',
        checked ? 'bg-primary' : 'bg-muted-foreground/30',
      )}
    >
      <span
        className={cn(
          'inline-block h-4 w-4 rounded-full bg-white shadow-sm transition-transform duration-[160ms]',
          checked ? 'translate-x-4' : 'translate-x-0.5',
        )}
      />
    </button>
  );
}

export function Settings() {
  const [activeTab, setActiveTab] = useState<SettingsTab>('workspace');
  const [biasLevel, setBiasLevel] = useState(3);
  const [notifications, setNotifications] = useState({ email: true, slack: false });

  const ActiveIcon = NAV_ITEMS.find(n => n.id === activeTab)?.icon ?? Building;

  return (
    <div className="space-y-0">
      <PageHeader
        title="Platform Settings"
        subtitle="Configure workspace, security, AI parameters, and integrations."
      />

      <div className="grid gap-6 md:grid-cols-[200px_1fr]">
        {/* ── Settings nav ── */}
        <nav aria-label="Settings navigation" className="space-y-0.5">
          {NAV_ITEMS.map(({ id, label, icon: Icon }) => {
            const isActive = activeTab === id;
            return (
              <button
                key={id}
                id={`settings-nav-${id}`}
                onClick={() => setActiveTab(id)}
                className={cn(
                  'relative w-full flex items-center gap-2.5 px-3 py-2 rounded-md text-left',
                  'text-body transition-colors duration-[120ms]',
                  'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring/50',
                  isActive
                    ? [
                        'bg-primary/8 text-primary font-medium',
                        'before:absolute before:left-0 before:top-1/2 before:-translate-y-1/2',
                        'before:w-0.5 before:h-4 before:rounded-r-full before:bg-primary',
                      ]
                    : 'text-muted-foreground hover:bg-muted/60 hover:text-foreground',
                )}
                aria-current={isActive ? 'page' : undefined}
              >
                <Icon className="h-4 w-4 shrink-0" aria-hidden="true" />
                <span className="truncate">{label}</span>
                {isActive && (
                  <ChevronRight className="h-3.5 w-3.5 ml-auto text-primary/50" aria-hidden="true" />
                )}
              </button>
            );
          })}
        </nav>

        {/* ── Settings panel ── */}
        <div className="space-y-5">

          {/* Workspace */}
          {activeTab === 'workspace' && (
            <Card>
              <CardHeader className="pb-0">
                <div className="flex items-center gap-2.5 mb-1">
                  <div className="h-8 w-8 rounded-lg bg-primary/10 border border-primary/20 flex items-center justify-center">
                    <Building className="h-4 w-4 text-primary" aria-hidden="true" />
                  </div>
                  <div>
                    <CardTitle>Workspace Profile</CardTitle>
                    <CardDescription>Manage your organization's core details.</CardDescription>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <FormRow label="Company Name" description="The legal entity name for your organization.">
                  <Input
                    id="company-name"
                    defaultValue="Acme Corp Enterprise"
                    aria-label="Company name"
                  />
                </FormRow>
                <FormRow label="Primary Domain" description="Your company's primary email domain.">
                  <Input
                    id="primary-domain"
                    defaultValue="acmecorp.com"
                    aria-label="Primary domain"
                  />
                </FormRow>
                <FormRow label="Fiscal Year End" description="Used for annual review cycle scheduling.">
                  <Input
                    id="fiscal-year"
                    type="month"
                    defaultValue="2026-12"
                    aria-label="Fiscal year end"
                  />
                </FormRow>
              </CardContent>
              <CardFooter className="border-t border-border/60">
                <Button size="sm">
                  <Save className="h-4 w-4" />
                  Save Changes
                </Button>
                <Button variant="ghost" size="sm">Discard</Button>
              </CardFooter>
            </Card>
          )}

          {/* AI Configuration */}
          {activeTab === 'ai' && (
            <Card>
              <CardHeader className="pb-0">
                <div className="flex items-center gap-2.5 mb-1">
                  <div className="h-8 w-8 rounded-lg bg-warning/10 border border-warning/20 flex items-center justify-center">
                    <Brain className="h-4 w-4 text-warning" aria-hidden="true" />
                  </div>
                  <div>
                    <CardTitle>AI Configuration</CardTitle>
                    <CardDescription>Adjust how FairTrace analyzes performance data.</CardDescription>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <FormRow
                  label="Bias Detection"
                  description="Higher sensitivity flags more potential bias patterns."
                >
                  <div className="space-y-2">
                    {/* Styled range slider */}
                    <div className="flex items-center gap-3">
                      <input
                        id="bias-sensitivity"
                        type="range"
                        min={1}
                        max={3}
                        step={1}
                        value={biasLevel}
                        onChange={(e) => setBiasLevel(Number(e.target.value))}
                        className={cn(
                          'flex-1 h-1.5 rounded-full appearance-none cursor-pointer',
                          'bg-muted accent-primary',
                        )}
                        aria-label="Bias detection sensitivity"
                        aria-valuetext={BIAS_LABELS[biasLevel]}
                      />
                      <span className={cn(
                        'text-label font-semibold px-2 py-0.5 rounded-md border min-w-[56px] text-center',
                        biasLevel === 1 ? 'bg-success/10 text-success border-success/20' :
                        biasLevel === 2 ? 'bg-warning/10 text-warning border-warning/20' :
                        'bg-primary/10 text-primary border-primary/20',
                      )}>
                        {BIAS_LABELS[biasLevel]}
                      </span>
                    </div>
                    <div className="flex justify-between text-caption text-muted-foreground/60 px-0.5">
                      <span>Low</span><span>Standard</span><span>High</span>
                    </div>
                  </div>
                </FormRow>
              </CardContent>
              <CardFooter className="border-t border-border/60">
                <Button size="sm">
                  <Save className="h-4 w-4" />
                  Save AI Settings
                </Button>
                <Button variant="ghost" size="sm">Reset to defaults</Button>
              </CardFooter>
            </Card>
          )}

          {/* Notifications */}
          {activeTab === 'notifications' && (
            <Card>
              <CardHeader className="pb-0">
                <div className="flex items-center gap-2.5 mb-1">
                  <div className="h-8 w-8 rounded-lg bg-info/10 border border-info/20 flex items-center justify-center">
                    <Bell className="h-4 w-4 text-info" aria-hidden="true" />
                  </div>
                  <div>
                    <CardTitle>Notifications</CardTitle>
                    <CardDescription>Configure how and where you receive alerts.</CardDescription>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <FormRow label="Email Notifications" description="Receive review cycle updates and approvals via email.">
                  <ToggleSwitch
                    id="email-notifications"
                    checked={notifications.email}
                    onChange={(v) => setNotifications(n => ({ ...n, email: v }))}
                  />
                </FormRow>
                <FormRow label="Slack Notifications" description="Connect to Slack for real-time pipeline alerts.">
                  <ToggleSwitch
                    id="slack-notifications"
                    checked={notifications.slack}
                    onChange={(v) => setNotifications(n => ({ ...n, slack: v }))}
                  />
                </FormRow>
              </CardContent>
              <CardFooter className="border-t border-border/60">
                <Button size="sm">
                  <Save className="h-4 w-4" />
                  Save Notifications
                </Button>
              </CardFooter>
            </Card>
          )}


        </div>
      </div>
    </div>
  );
}
