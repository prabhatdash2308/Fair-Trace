/**
 * LoginCard.tsx — Enterprise login page layout (Split-screen).
 *
 * Polished to "production-perfect":
 * - Vercel-like background (navy, noise, grid, radial glow)
 * - Trust metrics on left
 * - Elevated card with strong shadow on right
 * - SVG monochrome icons for SSO
 */
import * as React from 'react';
import { motion } from 'framer-motion';
import { ShieldCheck, Lock } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Separator } from '@/components/ui/separator';
import { LoginForm } from './LoginForm';
import { ThemeToggle } from '@/components/ui/ThemeToggle';

import { DemoCredentials } from './DemoCredentials';
import { APP_CAPABILITIES } from '@/config/capabilities';
import { ROUTES } from '@/constants/routes';
import { EASINGS } from '@/components/motion/variants';

import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';

const SSO_PROVIDERS = [
  {
    id: 'microsoft',
    name: 'Microsoft',
    icon: (
      <svg viewBox="0 0 21 21" className="w-4 h-4 fill-current opacity-80" xmlns="http://www.w3.org/2000/svg">
        <path d="M0 0h10v10H0zm11 0h10v10H11zm0 11h10v10H11zM0 11h10v10H0z" />
      </svg>
    ),
  },
  {
    id: 'google',
    name: 'Google',
    icon: (
      <svg viewBox="0 0 24 24" className="w-4 h-4 fill-current opacity-80" xmlns="http://www.w3.org/2000/svg">
        <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
        <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
        <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
        <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
      </svg>
    ),
  },
  {
    id: 'github',
    name: 'GitHub',
    icon: (
      <svg viewBox="0 0 24 24" className="w-4 h-4 fill-current opacity-80" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12" />
      </svg>
    ),
  },
];

export function LoginCard() {
  const subtitle = 'Enterprise Performance Intelligence';

  return (
    <div className="min-h-screen w-full flex flex-col lg:flex-row overflow-x-hidden selection:bg-primary/20 selection:text-primary bg-[#030712] relative">
      
      {/* Global Background Elements */}
      <div className="absolute inset-0 z-0 overflow-hidden pointer-events-none">
        {/* Radial glow */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-primary/10 rounded-full blur-[120px] opacity-50" />
        {/* Grid overlay */}
        <div className="absolute inset-0 opacity-[0.03]" style={{ backgroundImage: 'radial-gradient(hsl(var(--primary)) 1px, transparent 1px)', backgroundSize: '32px 32px' }} />
        {/* Noise texture (subtle) */}
        <div className="absolute inset-0 opacity-[0.02]" style={{ backgroundImage: 'url("data:image/svg+xml,%3Csvg viewBox=%220 0 200 200%22 xmlns=%22http://www.w3.org/2000/svg%22%3E%3Cfilter id=%22noiseFilter%22%3E%3CfeTurbulence type=%22fractalNoise%22 baseFrequency=%220.65%22 numOctaves=%223%22 stitchTiles=%22stitch%22/%3E%3C/filter%3E%3Crect width=%22100%25%22 height=%22100%25%22 filter=%22url(%23noiseFilter)%22/%3E%3C/svg%3E")' }} />
      </div>

      {/* ── Left Panel: Enterprise Branding ── */}
      <div className="relative z-10 hidden lg:flex flex-col justify-between w-full lg:w-1/2 p-16 overflow-y-auto border-r border-border/10 shadow-[inset_-20px_0_40px_rgba(0,0,0,0.2)] bg-card/10 backdrop-blur-[2px]">
        
        {/* Faint radial spotlight inside left panel */}
        <div className="absolute -left-40 top-40 w-[600px] h-[600px] bg-primary/5 rounded-full blur-[100px] pointer-events-none" />

        <div className="relative z-10 flex flex-col max-w-xl">
          {/* Brand */}
          <div className="flex items-center gap-3 mb-24">
            <div className="flex items-center justify-center h-10 w-10 rounded-lg bg-primary/10 border border-primary/20">
              <ShieldCheck className="h-5 w-5 text-primary" aria-hidden="true" />
            </div>
            <span className="text-xl font-bold tracking-tight text-white">ReviewGuard <span className="text-primary">AI</span></span>
          </div>

          <h1 className="text-5xl font-bold tracking-tight text-white mb-6 leading-[1.1]">
            Explainable AI<br />
            for Enterprise<br />
            Performance Reviews.
          </h1>
          <p className="text-lg text-muted-foreground/80 mb-16 max-w-md leading-relaxed font-medium">
            Generate transparent, explainable, and auditable employee performance reviews securely.
          </p>

          {/* Trust Metrics */}
          <div className="grid grid-cols-2 gap-x-8 gap-y-12">
            {[
              { stat: '99.99%', label: 'Availability' },
              { stat: 'SOC2', label: 'Ready' },
              { stat: 'ISO27001', label: 'Aligned' },
              { stat: '100%', label: 'Explainable' }
            ].map((metric) => (
              <div key={metric.label} className="flex flex-col">
                <span className="text-3xl font-bold text-white mb-1 tracking-tight">{metric.stat}</span>
                <span className="text-[13px] uppercase tracking-wider text-muted-foreground font-semibold">{metric.label}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Footer */}
        <div className="relative z-10 flex flex-wrap gap-6 text-[13px] font-semibold text-muted-foreground/60 pt-12">
          <span className="hover:text-foreground cursor-default transition-colors">Enterprise Edition</span>
          <span className="hover:text-foreground cursor-pointer transition-colors">Documentation</span>
          <span className="hover:text-foreground cursor-pointer transition-colors">Privacy</span>
          <span className="hover:text-foreground cursor-pointer transition-colors">Terms</span>
          <span className="hover:text-foreground cursor-default transition-colors">v2.4.0</span>
        </div>
      </div>

      {/* ── Right Panel: Authentication ── */}
      <div className="flex-1 flex flex-col items-center justify-center p-6 lg:p-12 relative z-10">
        <div className="absolute top-6 right-6 lg:top-12 lg:right-12">
          <ThemeToggle />
        </div>
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, ease: EASINGS.easeOut }}
          className="w-full max-w-[520px]"
        >
          {/* Mobile Brand Header */}
          <div className="lg:hidden flex flex-col items-center mb-8 text-center">
            <div className="flex items-center justify-center h-12 w-12 rounded-xl bg-primary/10 border border-primary/20 mb-4 shadow-lg shadow-primary/10">
              <ShieldCheck className="h-6 w-6 text-primary" aria-hidden="true" />
            </div>
            <h1 className="text-2xl font-bold text-white tracking-tight">ReviewGuard AI</h1>
          </div>

          {/* Authentication Card - High Elevation */}
          <div className="bg-card/70 backdrop-blur-xl border border-border/40 rounded-[28px] shadow-[0_24px_64px_-12px_rgba(0,0,0,0.5)] overflow-hidden flex flex-col relative z-20">
            
            {/* Soft inner highlight */}
            <div className="absolute inset-0 rounded-[28px] pointer-events-none border border-white/5" />

            {/* Header */}
            <div className="px-8 pt-10 pb-6 text-center border-b border-border/40 bg-card/30">
              <h2 className="text-2xl font-bold tracking-tight text-white mb-2">
                Sign in to ReviewGuard AI
              </h2>
              <motion.p
                key={subtitle}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.15 }}
                className="text-sm font-medium text-muted-foreground"
              >
                {subtitle}
              </motion.p>
            </div>

            {/* Form */}
            <div className="px-8 pt-8 pb-2">
              <LoginForm />
            </div>

            {/* Security Footer */}
            <div className="px-8 pb-8 flex flex-col items-center text-[11px] font-medium text-muted-foreground/50">
              <div className="flex items-center gap-1.5 mb-1.5">
                <Lock className="h-3 w-3" />
                <span>Protected by Enterprise Authentication</span>
              </div>
              <div className="flex gap-2">
                <span>AES-256 Encryption</span>
                <span>•</span>
                <span>Role-Based Access Control</span>
              </div>
            </div>

            {/* Divider */}
            <div className="px-8 pb-6 flex items-center gap-3">
              <Separator className="flex-1 opacity-50" />
              <span className="text-[10px] font-bold text-muted-foreground/60 uppercase tracking-widest whitespace-nowrap">
                Or continue with
              </span>
              <Separator className="flex-1 opacity-50" />
            </div>

            {/* Enterprise SSO */}
            <div className="px-8 pb-8">
              <div className="flex justify-center gap-4">
                <TooltipProvider delayDuration={200}>
                  {SSO_PROVIDERS.map((provider) => {
                    const key = provider.id as 'microsoft' | 'google' | 'github';
                    const isEnabled = APP_CAPABILITIES.auth.sso[key];
                    
                    const btn = (
                      <button
                        key={provider.id}
                        type="button"
                        disabled={!isEnabled}
                        className="flex items-center justify-center gap-2 h-11 w-full rounded-xl border border-border/50 bg-card/40 text-[13px] font-medium text-foreground disabled:opacity-40 disabled:cursor-not-allowed hover:bg-muted/80 hover:border-border transition-all duration-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring shadow-sm hover:shadow-md"
                      >
                        {provider.icon}
                        {provider.name}
                      </button>
                    );

                    return !isEnabled ? (
                      <Tooltip key={provider.id}>
                        <TooltipTrigger asChild>
                          <div className="w-full flex-1">{btn}</div>
                        </TooltipTrigger>
                        <TooltipContent side="bottom" className="text-xs bg-card border border-border">
                          Configured by your organization
                        </TooltipContent>
                      </Tooltip>
                    ) : (
                      <div className="w-full flex-1" key={provider.id}>{btn}</div>
                    );
                  })}
                </TooltipProvider>
              </div>
            </div>

            {/* Demo Accounts */}
            <div className="px-8 pb-8 bg-muted/10 border-t border-border/30 pt-6">
              <DemoCredentials />
            </div>
          </div>

          {/* Mobile/Auth Footer */}
          <div className="mt-8 flex flex-col items-center gap-4">
            <Link
              to={ROUTES.ROOT}
              className="text-[13px] font-semibold text-muted-foreground/80 hover:text-white transition-colors underline underline-offset-4 decoration-muted-foreground/40 hover:decoration-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring rounded-sm"
            >
              ← Back to home
            </Link>
            <div className="flex flex-wrap justify-center gap-x-4 gap-y-2 text-[11px] text-muted-foreground/60 font-semibold lg:hidden">
              <span className="hover:text-white cursor-default transition-colors">Enterprise Edition</span>
              <span className="hover:text-white cursor-pointer transition-colors">Privacy</span>
              <span className="hover:text-white cursor-pointer transition-colors">Terms</span>
            </div>
          </div>

        </motion.div>
      </div>
    </div>
  );
}
