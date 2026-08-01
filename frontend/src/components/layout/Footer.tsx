import { env } from '@/config/env';

/**
 * Footer — minimal placeholder with version information.
 * Positioned at the bottom of the content area inside AppLayout.
 */
export function Footer() {
  const year = new Date().getFullYear();

  return (
    <footer className="mt-auto border-t border-border bg-card px-8 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between text-xs text-muted-foreground">
        <span>© {year} ReviewGuard AI. All rights reserved.</span>
        <span className="font-mono">
          v{env.appVersion} · {env.appEnv}
        </span>
      </div>
    </footer>
  );
}
