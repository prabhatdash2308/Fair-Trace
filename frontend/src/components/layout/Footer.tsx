import { env } from '@/config/env';

/**
 * Footer — minimal placeholder with version information.
 * Positioned at the bottom of the content area inside AppLayout.
 */
export function Footer() {
  const year = new Date().getFullYear();

  return (
    <footer className="mt-auto border-t border-border bg-card/50 px-8 py-3">
      <div className="max-w-screen-xl mx-auto flex items-center justify-between">
        <span className="text-label text-muted-foreground/60">
          © {year} FairTrace. All rights reserved.
        </span>
        <span className="font-mono text-[10px] text-muted-foreground/40 tracking-wider">
          v{env.appVersion} · {env.appEnv}
        </span>
      </div>
    </footer>
  );
}
