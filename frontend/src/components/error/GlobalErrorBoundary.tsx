import { Component, type ReactNode } from 'react';
import { AlertOctagon, RefreshCw, Home, MessageSquareWarning } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class GlobalErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo);
  }

  private handleRetry = () => {
    this.setState({ hasError: false, error: undefined });
    window.location.reload();
  };
  
  private handleReportIssue = () => {
    // In a real app this might open an Intercom widget or mailto link
    window.location.href = 'mailto:support@fairtrace.ai?subject=Platform%20Crash%20Report';
  };

  public render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-background flex flex-col items-center justify-center p-6">
          <div className="max-w-xl w-full bg-card border border-border shadow-sm rounded-xl p-8 overflow-hidden">
            <div className="flex items-center gap-4 mb-6 pb-6 border-b border-border/50">
              <div className="h-12 w-12 bg-destructive/10 rounded-full flex items-center justify-center shrink-0">
                <AlertOctagon className="h-6 w-6 text-destructive" />
              </div>
              <div>
                <h1 className="text-xl font-semibold tracking-tight text-foreground">Something went wrong</h1>
                <p className="text-sm text-muted-foreground">The application encountered an unexpected fault.</p>
              </div>
            </div>

            <div className="space-y-6 mb-8">
              <div>
                <h2 className="text-sm font-medium text-foreground mb-1">What happened</h2>
                <p className="text-sm text-muted-foreground">
                  A critical error occurred while rendering the page. This prevents the interface from displaying correctly.
                </p>
              </div>
              
              <div>
                <h2 className="text-sm font-medium text-foreground mb-1">Possible causes</h2>
                <ul className="text-sm text-muted-foreground list-disc pl-5 space-y-1">
                  <li>Network connectivity issues</li>
                  <li>An outdated browser cache or stale session</li>
                  <li>A temporary backend outage</li>
                </ul>
              </div>
            </div>

            <div className="flex flex-wrap gap-3">
              <Button onClick={this.handleRetry} className="gap-2">
                <RefreshCw className="h-4 w-4" />
                Reload
              </Button>
              <Button variant="outline" onClick={() => window.location.href = '/'} className="gap-2">
                <Home className="h-4 w-4" />
                Go Home
              </Button>
              <Button variant="secondary" onClick={this.handleReportIssue} className="gap-2">
                <MessageSquareWarning className="h-4 w-4" />
                Report Issue
              </Button>
            </div>

            {import.meta.env.DEV && (
              <div className="mt-8 pt-6 border-t border-border/50">
                <h2 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3">Technical Details (Dev Only)</h2>
                <div className="bg-muted p-4 rounded-md overflow-x-auto text-[11px] font-mono text-muted-foreground leading-relaxed whitespace-pre">
                  {this.state.error?.stack || this.state.error?.toString()}
                </div>
              </div>
            )}
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

