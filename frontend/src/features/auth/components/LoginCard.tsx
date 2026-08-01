import { motion } from 'framer-motion';
import { ShieldCheck } from 'lucide-react';
import { Link } from 'react-router-dom';
import { GlassCard } from '@/components/cult/GlassCard';
import { LoginForm } from './LoginForm';
import { ROUTES } from '@/constants/routes';

/**
 * LoginCard — the Cult UI premium container for the auth form.
 * Cult UI used here intentionally — login page is a high-impact visual entry point.
 *
 * Layout:
 *  - Full-page centered background
 *  - GlassCard wraps the form (Cult UI — approved use case)
 *  - Framer Motion card entrance animation
 */
export function LoginCard() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-background px-4 py-12">
      {/* Subtle background grid pattern */}
      <div
        aria-hidden="true"
        className="pointer-events-none fixed inset-0 opacity-[0.03] dark:opacity-[0.06]"
        style={{
          backgroundImage:
            'linear-gradient(hsl(var(--foreground)) 1px, transparent 1px), linear-gradient(90deg, hsl(var(--foreground)) 1px, transparent 1px)',
          backgroundSize: '48px 48px',
        }}
      />

      <motion.div
        initial={{ opacity: 0, y: 20, scale: 0.97 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.35, ease: [0.4, 0, 0.2, 1] }}
        className="w-full max-w-md"
      >
        <GlassCard padding="lg" hoverable={false}>
          {/* ── Brand header ── */}
          <div className="flex flex-col items-center mb-8">
            <div className="flex items-center justify-center h-12 w-12 rounded-xl bg-primary/10 mb-4">
              <ShieldCheck className="h-6 w-6 text-primary" aria-hidden="true" />
            </div>
            <h1 className="text-2xl font-bold text-foreground tracking-tight">
              ReviewGuard AI
            </h1>
            <p className="mt-1 text-sm text-muted-foreground text-center">
              Sign in to your enterprise account
            </p>
          </div>

          {/* ── Login form ── */}
          <LoginForm />

          {/* ── Divider ── */}
          <div className="relative my-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-border" />
            </div>
            <div className="relative flex justify-center">
              <span className="px-3 bg-card text-xs text-muted-foreground">
                or continue with SSO
              </span>
            </div>
          </div>

          {/* ── SSO placeholder buttons ── */}
          <div className="grid grid-cols-2 gap-3">
            {(['Microsoft', 'Google'] as const).map((provider) => (
              <button
                key={provider}
                type="button"
                disabled
                aria-label={`Sign in with ${provider} — coming soon`}
                className="flex items-center justify-center gap-2 h-10 rounded-md border border-border bg-background text-sm text-muted-foreground opacity-60 cursor-not-allowed transition-colors"
              >
                {provider}
              </button>
            ))}
          </div>

          {/* ── Footer link ── */}
          <p className="mt-6 text-center text-xs text-muted-foreground">
            <Link
              to={ROUTES.ROOT}
              className="hover:text-foreground transition-colors underline underline-offset-2"
            >
              ← Back to home
            </Link>
          </p>
        </GlassCard>

        {/* Version note below the card */}
        <p className="mt-4 text-center text-xs text-muted-foreground">
          ReviewGuard AI · Enterprise Edition
        </p>
      </motion.div>
    </div>
  );
}
