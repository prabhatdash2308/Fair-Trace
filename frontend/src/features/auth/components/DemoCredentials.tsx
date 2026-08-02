/**
 * DemoCredentials.tsx — Tabs-based demo account credentials.
 *
 * Polished layout: Clean row structure (Email, ••••••••, Copy buttons).
 */
import * as React from 'react';
import { Copy, Check } from 'lucide-react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { useToast } from '@/components/ui/use-toast';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';

interface DemoAccount {
  role: string;
  email: string;
  password: string;
}

const DEMO_ACCOUNTS: DemoAccount[] = [
  { role: 'Administrator', email: 'admin@reviewguard.ai', password: 'admin123456' },
  { role: 'Manager',       email: 'manager@reviewguard.ai', password: 'manager123456' },
  { role: 'Employee',      email: 'employee@reviewguard.ai', password: 'employee123456' },
];

function CopyButton({ value, label }: { value: string; label: string }) {
  const { toast } = useToast();
  const [copied, setCopied] = React.useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(value);
      setCopied(true);
      toast({
        title: 'Copied to clipboard',
        description: `The ${label.toLowerCase()} has been copied.`,
      });
      setTimeout(() => setCopied(false), 2000);
    } catch {
      const el = document.createElement('textarea');
      el.value = value;
      document.body.appendChild(el);
      el.select();
      document.execCommand('copy');
      document.body.removeChild(el);
      setCopied(true);
      toast({
        title: 'Copied to clipboard',
        description: `The ${label.toLowerCase()} has been copied.`,
      });
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <Button
      variant="outline"
      size="sm"
      type="button"
      onClick={handleCopy}
      aria-label={`Copy ${label}`}
      className={cn(
        'h-7 px-2.5 text-[11px] font-semibold flex items-center gap-1.5 transition-colors',
        copied ? 'bg-success/10 text-success border-success/30 hover:bg-success/20 hover:text-success' : 'text-muted-foreground bg-background hover:bg-muted/80'
      )}
    >
      {copied ? <Check className="h-3 w-3" /> : <Copy className="h-3 w-3" />}
      Copy {label}
    </Button>
  );
}

export function DemoCredentials() {
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <p className="text-[11px] font-semibold text-muted-foreground/60 uppercase tracking-widest">
          Demo Accounts
        </p>
      </div>
      
      <Tabs defaultValue="Administrator" className="w-full">
        <TabsList className="w-full grid grid-cols-3 mb-4 h-9 bg-card border border-border/50">
          {DEMO_ACCOUNTS.map((account) => (
            <TabsTrigger key={account.role} value={account.role} className="text-[11px] font-semibold tracking-wide">
              {account.role}
            </TabsTrigger>
          ))}
        </TabsList>
        
        {DEMO_ACCOUNTS.map((account) => (
          <TabsContent key={account.role} value={account.role} className="mt-0 outline-none">
            <div className="rounded-xl border border-border/50 bg-card p-4 space-y-4 shadow-sm">
              <div className="flex flex-col gap-3">
                <div className="flex items-center justify-between">
                  <code className="text-sm font-mono text-foreground truncate font-medium bg-background px-2 py-1 rounded border border-border/40">{account.email}</code>
                  <CopyButton value={account.email} label="Email" />
                </div>
                <div className="flex items-center justify-between">
                  <code className="text-sm font-mono text-muted-foreground truncate bg-background px-2 py-1 rounded border border-border/40 tracking-widest">••••••••</code>
                  <CopyButton value={account.password} label="Password" />
                </div>
              </div>
            </div>
            <p className="text-[11px] text-muted-foreground/60 mt-3 text-center font-medium">
              Please paste these credentials manually.
            </p>
          </TabsContent>
        ))}
      </Tabs>
    </div>
  );
}
