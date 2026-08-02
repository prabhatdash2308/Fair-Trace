/**
 * LandingPage.tsx — Enterprise Production Landing Page
 *
 * Architecture:
 * - Two-column hero: Left (headline + CTAs + trust badges) | Right (live AI pipeline)
 * - Per-section unique backgrounds (no global fixed overlay)
 * - shadcn/ui: Accordion (FAQ), Tooltip (pipeline nodes), Badge (trust signals), Sheet (mobile nav)
 * - Motion: useReducedMotion, standardized TIMINGS, no bounce
 * - Accessibility: landmarks, ARIA, skip-nav, keyboard nav
 * - Performance: useCallback, memo, no unnecessary rerenders
 */

import * as React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useReducedMotion, motion, useScroll, useTransform, AnimatePresence } from 'framer-motion';
import {
  ShieldCheck, ArrowRight, BrainCircuit, Activity, Lock, ExternalLink,
  Target, Database, FileText, CheckCircle2, Zap, AlertTriangle, Users,
  Menu, X, ChevronDown, UserCheck, Bot, Layers, GitBranch, Eye
} from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { ThemeToggle } from '@/components/ui/ThemeToggle';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion';
import {
  Sheet,
  SheetContent,
  SheetTrigger,
} from '@/components/ui/sheet';

import { useAuthStore } from '@/store/auth/auth.store';
import { ROUTES } from '@/constants/routes';
import { EASINGS, TIMINGS } from '@/components/motion/variants';

// ─── Smooth scroll utility ───────────────────────────────────────────────────
function smoothScrollTo(id: string) {
  const el = document.getElementById(id);
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ─── Pipeline stage data ─────────────────────────────────────────────────────
const PIPELINE_STAGES = [
  {
    id: 'input',
    label: 'Employee Data',
    sublabel: 'Review + Peer Feedback',
    icon: FileText,
    color: 'text-primary',
    tooltip: 'Structured and unstructured review inputs are securely ingested from HR systems.',
  },
  {
    id: 'retrieval',
    label: 'Retrieval',
    sublabel: 'Vector Database',
    icon: Database,
    color: 'text-primary',
    tooltip: 'Historical performance data is retrieved via semantic similarity from a private vector store.',
  },
  {
    id: 'analysis',
    label: 'AI Analysis',
    sublabel: 'LangGraph Agents',
    icon: BrainCircuit,
    color: 'text-primary',
    tooltip: 'Parallel LangGraph agents evaluate competency dimensions and cross-reference peer inputs.',
  },
  {
    id: 'bias',
    label: 'Bias Detection',
    sublabel: 'Recency · Halo · Horn',
    icon: Activity,
    color: 'text-warning',
    tooltip: 'Automated detection of 7 known cognitive bias patterns with severity scoring.',
  },
  {
    id: 'explainability',
    label: 'Explainability',
    sublabel: 'Evidence Tracing',
    icon: Eye,
    color: 'text-primary',
    tooltip: 'Every claim is linked back to the exact source sentence that generated it.',
  },
  {
    id: 'approval',
    label: 'Human Approval',
    sublabel: 'Manager Review',
    icon: UserCheck,
    color: 'text-success',
    tooltip: 'The final decision always remains with a human manager before the report is finalized.',
  },
] as const;

// ─── Live AI Pipeline Visualization ─────────────────────────────────────────
const AIPipelineVisual = React.memo(function AIPipelineVisual() {
  const shouldReduceMotion = useReducedMotion();
  const [activeStage, setActiveStage] = React.useState<number | null>(null);

  return (
    <TooltipProvider delayDuration={200}>
      <div
        role="img"
        aria-label="Live AI pipeline visualization showing 6 processing stages from Employee Data to Human Approval"
        className="relative w-full max-w-sm mx-auto"
      >
        {/* Connector line — vertical axis */}
        <div
          className="absolute left-6 top-8 bottom-8 w-px bg-gradient-to-b from-primary/30 via-primary/20 to-success/30"
          aria-hidden="true"
        />

        {/* Stage nodes */}
        <div className="flex flex-col gap-3">
          {PIPELINE_STAGES.map((stage, i) => {
            const Icon = stage.icon;
            const isActive = activeStage === i;
            return (
              <motion.div
                key={stage.id}
                initial={shouldReduceMotion ? { opacity: 1 } : { opacity: 0, x: 12 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{
                  delay: shouldReduceMotion ? 0 : 0.3 + i * 0.1,
                  duration: TIMINGS.CARD,
                  ease: EASINGS.easeOut,
                }}
              >
                <Tooltip>
                  <TooltipTrigger asChild>
                    <button
                      className={[
                        'w-full flex items-center gap-4 px-4 py-3 rounded-xl border transition-all text-left',
                        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
                        isActive
                          ? 'border-primary/40 bg-primary/5 shadow-sm'
                          : 'border-border/60 bg-card/60 hover:border-border hover:bg-card',
                        !shouldReduceMotion && 'motion-safe:transition-all',
                      ].join(' ')}
                      onMouseEnter={() => setActiveStage(i)}
                      onMouseLeave={() => setActiveStage(null)}
                      onFocus={() => setActiveStage(i)}
                      onBlur={() => setActiveStage(null)}
                      aria-pressed={isActive}
                      type="button"
                    >
                      {/* Icon bubble */}
                      <div className={[
                        'relative z-10 flex items-center justify-center w-8 h-8 rounded-full border-2 border-border bg-background flex-shrink-0',
                        !shouldReduceMotion && isActive ? 'pipeline-pulse' : '',
                      ].join(' ')}>
                        <Icon className={`h-4 w-4 ${stage.color}`} aria-hidden="true" />
                      </div>

                      {/* Label */}
                      <div className="min-w-0">
                        <p className="text-caption font-semibold text-foreground leading-none">
                          {stage.label}
                        </p>
                        <p className="text-label text-muted-foreground mt-1 truncate">
                          {stage.sublabel}
                        </p>
                      </div>

                      {/* Active indicator */}
                      <AnimatePresence>
                        {isActive && (
                          <motion.div
                            initial={{ opacity: 0, scale: 0.8 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.8 }}
                            transition={{ duration: TIMINGS.HOVER }}
                            className="ml-auto flex-shrink-0 h-1.5 w-1.5 rounded-full bg-primary"
                            aria-hidden="true"
                          />
                        )}
                      </AnimatePresence>
                    </button>
                  </TooltipTrigger>
                  <TooltipContent side="right" className="max-w-[200px] text-xs">
                    {stage.tooltip}
                  </TooltipContent>
                </Tooltip>
              </motion.div>
            );
          })}
        </div>

        {/* Final output badge */}
        <motion.div
          initial={shouldReduceMotion ? { opacity: 1 } : { opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: shouldReduceMotion ? 0 : 1.0, duration: TIMINGS.PAGE }}
          className="mt-4 flex items-center gap-3 px-4 py-3 rounded-xl border border-success/30 bg-success/5"
        >
          <div className="flex items-center justify-center w-8 h-8 rounded-full border-2 border-success/40 bg-background flex-shrink-0">
            <ShieldCheck className="h-4 w-4 text-success" aria-hidden="true" />
          </div>
          <div>
            <p className="text-caption font-semibold text-foreground leading-none">Final Report</p>
            <p className="text-label text-muted-foreground mt-1">Auditable · Explainable · Signed</p>
          </div>
          <div className="ml-auto">
            <span className="inline-flex items-center gap-1 text-label text-success font-medium">
              <CheckCircle2 className="h-3 w-3" aria-hidden="true" />
              Ready
            </span>
          </div>
        </motion.div>
      </div>
    </TooltipProvider>
  );
});

// ─── Trust Badges ─────────────────────────────────────────────────────────────
const TRUST_BADGES = [
  { label: 'SOC2 Type II' },
  { label: 'GDPR Ready' },
  { label: 'ISO 27001' },
  { label: 'Private Deployment' },
] as const;

// ─── Nav links ────────────────────────────────────────────────────────────────
const NAV_LINKS = [
  { id: 'problem',        label: 'The Problem' },
  { id: 'how-it-works',   label: 'Platform' },
  { id: 'explainability', label: 'Explainability' },
  { id: 'security',       label: 'Security' },
] as const;

// ─── FAQ data ─────────────────────────────────────────────────────────────────
const FAQ_ITEMS = [
  {
    q: 'Does ReviewGuard replace human managers?',
    a: 'No. ReviewGuard acts as an impartial copilot. It surfaces evidence, flags biases, and standardizes formatting. The final performance rating is always approved and signed by a human manager.',
  },
  {
    q: 'Is our review data used to train public models?',
    a: 'Absolutely not. Your data belongs exclusively to your organization. All inference occurs in your private deployment. Nothing is ever sent to public model providers for training.',
  },
  {
    q: 'How long does enterprise implementation take?',
    a: 'Typical enterprise deployments take 2–4 weeks, including SSO integration, HRIS connector setup, and ingestion of historical review data.',
  },
  {
    q: 'How is AI bias detected and remediated?',
    a: 'ReviewGuard detects 7 known cognitive bias patterns (recency, halo, horn, leniency, severity, imbalance, and unsupported claims) with confidence scores. Each detection links back to the source text that triggered it.',
  },
  {
    q: 'What HRIS systems does ReviewGuard integrate with?',
    a: 'We provide native connectors for Workday, BambooHR, Lattice, and Slack. Custom SCIM/SAML integrations are available for enterprise deployments.',
  },
] as const;

// ─── Main LandingPage component ───────────────────────────────────────────────
export function LandingPage() {
  const { isAuthenticated } = useAuthStore();
  const navigate = useNavigate();
  const { scrollY } = useScroll();
  const headerOpacity = useTransform(scrollY, [0, 60], [0, 1]);
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false);

  const handleCTA = React.useCallback(() => {
    navigate(isAuthenticated ? ROUTES.DASHBOARD : ROUTES.LOGIN);
  }, [isAuthenticated, navigate]);

  return (
    <div className="min-h-screen bg-background flex flex-col font-sans overflow-x-hidden">
      {/* ── Skip Navigation ─────────────────────────────────────────────── */}
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-[100] focus:px-4 focus:py-2 focus:bg-primary focus:text-primary-foreground focus:rounded-md focus:text-sm focus:font-medium"
      >
        Skip to main content
      </a>

      {/* ── Navbar ──────────────────────────────────────────────────────── */}
      <header
        role="banner"
        className="fixed top-0 left-0 right-0 z-50"
      >
        <motion.div
          className="absolute inset-0 bg-background/85 backdrop-blur-xl border-b border-border"
          style={{ opacity: headerOpacity }}
          aria-hidden="true"
        />
        <div className="relative max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          {/* Logo */}
          <button
            className="flex items-center gap-2 group focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 rounded-sm"
            onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
            aria-label="ReviewGuard AI — scroll to top"
          >
            <ShieldCheck className="h-5 w-5 text-foreground group-hover:text-primary motion-safe:transition-colors" aria-hidden="true" />
            <span className="text-base font-bold tracking-tight">ReviewGuard AI</span>
          </button>

          {/* Desktop Nav */}
          <nav aria-label="Primary navigation" className="hidden md:flex items-center gap-8 text-caption font-medium text-muted-foreground">
            {NAV_LINKS.map(link => (
              <button
                key={link.id}
                id={`nav-link-${link.id}`}
                onClick={() => smoothScrollTo(link.id)}
                className="hover:text-foreground motion-safe:transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 rounded-sm px-1"
              >
                {link.label}
              </button>
            ))}
          </nav>

          {/* Desktop CTA */}
          <div className="hidden md:flex items-center gap-3">
            <ThemeToggle />
            {isAuthenticated ? (
              <Button
                id="btn-dashboard-nav"
                onClick={() => navigate(ROUTES.DASHBOARD)}
                variant="outline"
                size="sm"
                className="h-8 shadow-sm"
              >
                Go to Dashboard
              </Button>
            ) : (
              <Link
                id="link-signin-nav"
                to={ROUTES.LOGIN}
                className="text-caption font-medium text-muted-foreground hover:text-foreground motion-safe:transition-colors px-3 py-2 rounded-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              >
                Sign In
              </Link>
            )}
          </div>

          {/* Mobile Nav — Sheet */}
          <Sheet open={mobileMenuOpen} onOpenChange={setMobileMenuOpen}>
            <SheetTrigger asChild>
              <Button
                variant="ghost"
                size="sm"
                className="md:hidden h-8 w-8 p-0"
                aria-label={mobileMenuOpen ? 'Close navigation menu' : 'Open navigation menu'}
              >
                {mobileMenuOpen ? <X className="h-4 w-4" aria-hidden="true" /> : <Menu className="h-4 w-4" aria-hidden="true" />}
              </Button>
            </SheetTrigger>
            <SheetContent side="right" className="w-72 pt-16">
              <nav aria-label="Mobile navigation" className="flex flex-col gap-1">
                {NAV_LINKS.map(link => (
                  <button
                    key={link.id}
                    onClick={() => { smoothScrollTo(link.id); setMobileMenuOpen(false); }}
                    className="flex items-center gap-3 px-4 py-3 rounded-lg text-body font-medium text-muted-foreground hover:text-foreground hover:bg-muted/50 motion-safe:transition-colors text-left focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                  >
                    {link.label}
                  </button>
                ))}
                <div className="border-t border-border mt-4 pt-4">
                  {isAuthenticated ? (
                    <Button onClick={() => { navigate(ROUTES.DASHBOARD); setMobileMenuOpen(false); }} className="w-full">
                      Go to Dashboard
                    </Button>
                  ) : (
                    <Link to={ROUTES.LOGIN} onClick={() => setMobileMenuOpen(false)}>
                      <Button variant="outline" className="w-full">Sign In</Button>
                    </Link>
                  )}
                </div>
              </nav>
            </SheetContent>
          </Sheet>
        </div>
      </header>

      {/* ── Main Content ────────────────────────────────────────────────── */}
      <main id="main-content" role="main" className="flex-1 flex flex-col pt-16">

        {/* ── 1. HERO — Why should I care? ──────────────────────────────── */}
        <section
          aria-labelledby="hero-headline"
          className="hero-gradient relative overflow-hidden"
        >
          {/* Spotlight orb */}
          <div
            className="absolute -top-40 left-1/2 -translate-x-1/2 h-[500px] w-[500px] rounded-full bg-primary/10 blur-[120px] pointer-events-none"
            aria-hidden="true"
          />

          <div className="relative max-w-7xl mx-auto px-6 py-16 md:py-24">
            <div className="grid md:grid-cols-2 gap-12 lg:gap-20 items-center min-h-[70vh] md:min-h-[65vh]">

              {/* Left: Copy */}
              <motion.div
                initial={{ opacity: 0, y: 16 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: TIMINGS.PAGE, ease: EASINGS.easeOut }}
                className="flex flex-col gap-6 order-2 md:order-1"
              >
                {/* Eyebrow */}
                <div>
                  <Badge variant="secondary" className="text-label font-semibold tracking-wider uppercase px-3 py-1">
                    Enterprise AI Platform
                  </Badge>
                </div>

                {/* Headline */}
                <div className="space-y-3">
                  <h1
                    id="hero-headline"
                    className="text-display-lg md:text-display-xl text-foreground text-balance"
                  >
                    Performance reviews,<br />
                    <span className="text-primary">engineered</span> for precision.
                  </h1>
                  <p className="text-body-lg text-muted-foreground max-w-lg leading-relaxed">
                    Eliminate cognitive bias and standardize evaluations across your enterprise
                    with deterministic, explainable AI intelligence your legal team can trust.
                  </p>
                </div>

                {/* CTAs */}
                <div className="flex flex-col sm:flex-row gap-3">
                  <Link
                    id="btn-hero-primary"
                    to={isAuthenticated ? ROUTES.DASHBOARD : ROUTES.LOGIN}
                    className="inline-flex items-center justify-center rounded-md font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-11 px-8 text-caption group"
                  >
                    Deploy Intelligence
                    <ArrowRight className="ml-2 h-4 w-4 opacity-70 group-hover:translate-x-1 motion-safe:transition-transform" aria-hidden="true" />
                  </Link>
                  <Button
                    id="btn-hero-secondary"
                    size="lg"
                    variant="outline"
                    className="h-11 px-8 text-caption"
                    onClick={() => smoothScrollTo('how-it-works')}
                  >
                    See How It Works
                  </Button>
                </div>

                {/* Trust badges */}
                <div role="list" aria-label="Enterprise certifications" className="flex flex-wrap gap-2">
                  {TRUST_BADGES.map(badge => (
                    <Badge
                      key={badge.label}
                      role="listitem"
                      variant="outline"
                      className="text-label text-muted-foreground font-medium px-2.5 py-1 border-border/80"
                    >
                      <ShieldCheck className="h-3 w-3 mr-1.5 text-success" aria-hidden="true" />
                      {badge.label}
                    </Badge>
                  ))}
                </div>
              </motion.div>

              {/* Right: Live pipeline */}
              <motion.div
                initial={{ opacity: 0, x: 16 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: TIMINGS.PAGE, ease: EASINGS.easeOut, delay: 0.15 }}
                className="order-1 md:order-2"
              >
                {/* Pipeline card */}
                <div className="glass-surface border border-border/60 rounded-2xl p-6 shadow-lg">
                  <div className="flex items-center justify-between mb-5 pb-4 border-b border-border/50">
                    <div>
                      <p className="text-caption font-semibold text-foreground">AI Pipeline</p>
                      <p className="text-label text-muted-foreground mt-0.5">Hover to inspect each stage</p>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <div className="h-2 w-2 rounded-full bg-success pipeline-pulse" aria-hidden="true" />
                      <span className="text-label text-muted-foreground">Live</span>
                    </div>
                  </div>
                  <AIPipelineVisual />
                </div>
              </motion.div>
            </div>
          </div>
        </section>

        {/* ── 2. PROBLEM — Why is current HR broken? ──────────────────── */}
        <section
          id="problem"
          aria-labelledby="problem-heading"
          className="relative border-y border-border"
        >
          {/* Subtle dark background */}
          <div className="absolute inset-0 bg-foreground/[0.02]" aria-hidden="true" />
          <div className="relative max-w-7xl mx-auto px-6 py-16 md:py-20">
            <div className="grid md:grid-cols-2 gap-12 items-start">
              <div className="space-y-4">
                <h2 id="problem-heading" className="text-heading-xl tracking-tight text-balance">
                  The structural flaw in human evaluation.
                </h2>
                <p className="text-body-lg text-muted-foreground leading-relaxed">
                  Human evaluations are fundamentally susceptible to cognitive distortion. Recency bias,
                  halo effects, and inconsistent standards create an unfair environment that damages
                  retention, limits organizational velocity, and exposes companies to compliance risk.
                </p>
              </div>
              {/* Bias stat cards */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4" role="list" aria-label="Performance review statistics">
                {[
                  { stat: '87%', desc: 'of employees say reviews feel subjective', color: 'text-danger' },
                  { stat: '3.2×', desc: 'higher attrition after unfair review cycles', color: 'text-warning' },
                  { stat: '$420K', desc: 'average cost of a wrongful termination claim', color: 'text-primary' },
                ].map(item => (
                  <div
                    key={item.stat}
                    role="listitem"
                    className="p-5 rounded-xl border border-border bg-card shadow-sm"
                  >
                    <p className={`text-heading-lg font-bold ${item.color}`}>{item.stat}</p>
                    <p className="text-caption text-muted-foreground mt-1 leading-snug">{item.desc}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* ── 3. WHY AI FAILS — Why generic LLMs fail ─────────────────── */}
        <section aria-labelledby="ai-fail-heading" className="relative">
          <div className="absolute inset-0 bg-muted/20" aria-hidden="true" />
          <div className="relative max-w-7xl mx-auto px-6 py-16 md:py-20">
            <div className="grid md:grid-cols-2 gap-12 lg:gap-20 items-center">
              <div className="space-y-5">
                <AlertTriangle className="h-8 w-8 text-warning" aria-hidden="true" />
                <h2 id="ai-fail-heading" className="text-heading-lg tracking-tight">
                  Why generic AI fails at HR.
                </h2>
                <p className="text-body text-muted-foreground leading-relaxed">
                  Chatbot-generated reviews hallucinate facts, lack organizational context, and produce
                  output that cannot be traced back to evidence. That's not an AI problem — it's an
                  architecture problem. You need a deterministic pipeline, not a stochastic model.
                </p>
              </div>
              <div className="bg-card border border-border rounded-2xl shadow-sm overflow-hidden">
                <div className="px-6 py-4 border-b border-border bg-muted/30">
                  <p className="text-caption font-semibold text-foreground">Comparison</p>
                </div>
                <div className="divide-y divide-border">
                  {[
                    { label: 'Hallucination risk',   generic: 'High', rg: 'None', better: true },
                    { label: 'Source traceability',  generic: 'None', rg: 'Full', better: true },
                    { label: 'Bias detection',        generic: 'None', rg: 'Built-in', better: true },
                    { label: 'Audit trail',           generic: 'None', rg: 'Cryptographic', better: true },
                    { label: 'Human approval step',  generic: 'None', rg: 'Required', better: true },
                  ].map(row => (
                    <div key={row.label} className="grid grid-cols-3 px-6 py-3 text-caption">
                      <span className="text-muted-foreground">{row.label}</span>
                      <span className="text-danger font-medium">{row.generic}</span>
                      <span className="text-success font-medium">{row.rg}</span>
                    </div>
                  ))}
                  <div className="grid grid-cols-3 px-6 py-3 text-caption bg-muted/20 font-semibold text-foreground">
                    <span />
                    <span>Generic LLM</span>
                    <span>ReviewGuard AI</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ── 4. PLATFORM — How does ReviewGuard solve this? ────────────── */}
        <section
          id="how-it-works"
          aria-labelledby="platform-heading"
          className="relative border-t border-border"
        >
          {/* Glass panel background */}
          <div className="absolute inset-0 section-mesh opacity-[0.015]" aria-hidden="true" />
          <div className="relative max-w-7xl mx-auto px-6 py-16 md:py-24">
            <div className="text-center mb-12 max-w-3xl mx-auto">
              <h2 id="platform-heading" className="text-heading-xl tracking-tight mb-4">
                Intelligence at Enterprise Scale
              </h2>
              <p className="text-body-lg text-muted-foreground">
                Our multi-agent architecture ingests, processes, and evaluates performance data
                against your organizational rubric — with full auditability at every step.
              </p>
            </div>
            <div className="grid md:grid-cols-3 gap-6">
              {[
                {
                  icon: Database,
                  title: 'Data Ingestion',
                  number: '01',
                  desc: 'Securely aggregate employee reviews, peer feedback, and operational metrics into a private high-dimensional vector space.',
                },
                {
                  icon: BrainCircuit,
                  title: 'Multi-Agent Analysis',
                  number: '02',
                  desc: 'Parallel LangGraph agents evaluate competency dimensions, identify behavioral drift, and cross-reference peer inputs.',
                },
                {
                  icon: ShieldCheck,
                  title: 'Cryptographic Governance',
                  number: '03',
                  desc: 'Every insight is cryptographically hashed and mapped directly to the source evidence for perfect auditability.',
                },
              ].map((item, i) => (
                <motion.article
                  key={item.number}
                  initial={{ opacity: 0, y: 16 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true, margin: '-40px' }}
                  transition={{ delay: i * 0.08, duration: TIMINGS.PAGE, ease: EASINGS.easeOut }}
                  aria-labelledby={`platform-card-${item.number}`}
                  className="group relative p-8 border border-border rounded-2xl bg-card shadow-sm hover:border-primary/40 hover:shadow-md motion-safe:transition-all"
                >
                  <div className="flex items-start justify-between mb-6">
                    <div className="flex items-center justify-center w-10 h-10 rounded-xl bg-muted border border-border">
                      <item.icon className="h-5 w-5 text-foreground group-hover:text-primary motion-safe:transition-colors" aria-hidden="true" />
                    </div>
                    <span className="text-label font-semibold text-muted-foreground/50 tabular-nums">{item.number}</span>
                  </div>
                  <h3 id={`platform-card-${item.number}`} className="text-heading-sm mb-3">{item.title}</h3>
                  <p className="text-body text-muted-foreground leading-relaxed">{item.desc}</p>
                </motion.article>
              ))}
            </div>
          </div>
        </section>

        {/* ── 5. EXPLAINABILITY — Why can I trust it? ─────────────────── */}
        <section
          id="explainability"
          aria-labelledby="explainability-heading"
          className="relative border-t border-border"
        >
          {/* Soft spotlight background */}
          <div className="absolute inset-0 bg-gradient-to-br from-primary/[0.03] via-transparent to-transparent" aria-hidden="true" />
          <div className="relative max-w-7xl mx-auto px-6 py-16 md:py-24">
            <div className="grid md:grid-cols-2 gap-12 lg:gap-20 items-center">
              <div className="space-y-6">
                <h2 id="explainability-heading" className="text-heading-xl tracking-tight">
                  Radical Explainability
                </h2>
                <p className="text-body-lg text-muted-foreground leading-relaxed">
                  Black-box AI has no place in Human Resources. Every decision, score adjustment,
                  and promotion recommendation generated by ReviewGuard is fully explainable.
                  Managers can traverse the reasoning chain down to the exact sentence that
                  triggered a bias alert.
                </p>
                <ul className="space-y-3" aria-label="Explainability features">
                  {[
                    'Every claim linked to source text',
                    'Confidence score per insight',
                    'Full bias detection reasoning',
                    'Audit log for every AI action',
                  ].map(f => (
                    <li key={f} className="flex items-center gap-3 text-body text-muted-foreground">
                      <CheckCircle2 className="h-4 w-4 text-success flex-shrink-0" aria-hidden="true" />
                      {f}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Evidence card */}
              <div
                className="rounded-2xl border border-border bg-card shadow-md overflow-hidden"
                role="figure"
                aria-label="Example bias detection output"
              >
                <div className="flex items-center justify-between px-5 py-4 border-b border-border bg-muted/30">
                  <div className="flex items-center gap-2">
                    <Activity className="h-4 w-4 text-warning" aria-hidden="true" />
                    <span className="text-caption font-semibold">Bias Alert Detected</span>
                  </div>
                  <Badge variant="secondary" className="text-label">Severity: Medium</Badge>
                </div>
                <div className="p-5 space-y-4 font-mono text-caption text-muted-foreground">
                  <div className="grid grid-cols-[auto_1fr] gap-x-4 gap-y-2">
                    <span className="text-foreground font-medium font-sans">Type</span>
                    <span>Recency Bias</span>
                    <span className="text-foreground font-medium font-sans">Confidence</span>
                    <span>0.94</span>
                    <span className="text-foreground font-medium font-sans">Dimension</span>
                    <span>Performance Consistency</span>
                  </div>
                  <div className="p-3 rounded-lg bg-warning/5 border border-warning/20">
                    <p className="text-label font-medium text-warning font-sans mb-1">Evidence</p>
                    <p className="text-caption">&ldquo;Has performed exceptionally well over the last 3 weeks...&rdquo;</p>
                  </div>
                  <div className="p-3 rounded-lg bg-muted border border-border">
                    <p className="text-label font-medium text-foreground font-sans mb-1">Resolution</p>
                    <p className="text-caption font-sans text-muted-foreground">
                      Adjust score to reflect the full 6-month cycle rather than isolated recent performance.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ── 6. GOVERNANCE — How is every decision auditable? ─────────── */}
        <section aria-labelledby="governance-heading" className="relative border-t border-border">
          <div className="absolute inset-0 bg-foreground/[0.02]" aria-hidden="true" />
          <div className="relative max-w-7xl mx-auto px-6 py-16 md:py-20">
            <div className="grid md:grid-cols-3 gap-8 items-start">
              <div className="md:col-span-1 space-y-4">
                <Users className="h-8 w-8 text-primary" aria-hidden="true" />
                <h2 id="governance-heading" className="text-heading-lg tracking-tight">
                  Human in the Loop, Always.
                </h2>
                <p className="text-body text-muted-foreground leading-relaxed">
                  ReviewGuard AI acts as an impartial copilot. The final decision always remains
                  with human leadership.
                </p>
              </div>
              <div className="md:col-span-2 grid sm:grid-cols-2 gap-4">
                {[
                  { icon: Eye,       title: 'Full Audit Trail',     desc: 'Every AI action is timestamped, signed, and logged immutably.' },
                  { icon: GitBranch, title: 'Version Control',      desc: 'Each report version is retained with a diff of all changes.' },
                  { icon: UserCheck, title: 'Manager Approval',     desc: 'No report is finalized without explicit human sign-off.' },
                  { icon: Layers,    title: 'Role-Based Access',    desc: 'Granular RBAC ensures the right people see the right data.' },
                ].map(item => (
                  <div key={item.title} className="p-5 rounded-xl border border-border bg-card shadow-sm">
                    <item.icon className="h-5 w-5 text-muted-foreground mb-3" aria-hidden="true" />
                    <h3 className="text-caption font-semibold text-foreground mb-1">{item.title}</h3>
                    <p className="text-caption text-muted-foreground leading-relaxed">{item.desc}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* ── 7. SECURITY — Can my enterprise deploy this? ─────────────── */}
        <section
          id="security"
          aria-labelledby="security-heading"
          className="relative border-t border-border bg-foreground text-background"
        >
          <div className="absolute inset-0 bg-gradient-to-br from-foreground via-foreground to-foreground/90" aria-hidden="true" />
          <div className="relative max-w-7xl mx-auto px-6 py-16 md:py-24">
            <div className="grid md:grid-cols-2 gap-12 lg:gap-20 items-center">
              <div className="space-y-6">
                <Lock className="h-8 w-8 text-background/70" aria-hidden="true" />
                <h2 id="security-heading" className="text-heading-xl tracking-tight text-background">
                  Zero-Trust Enterprise Security
                </h2>
                <p className="text-body-lg text-background/70 leading-relaxed">
                  We process highly sensitive HR data. ReviewGuard AI is built on a zero-trust
                  architecture with end-to-end encryption and strict data residency controls.
                  Your performance data never trains public models.
                </p>
              </div>
              <div className="grid sm:grid-cols-2 gap-4">
                {[
                  { label: 'SOC2 Type II',          desc: 'Annual third-party security audit' },
                  { label: 'GDPR Ready',             desc: 'Data residency and right-to-erasure controls' },
                  { label: 'ISO 27001',              desc: 'Information security management certified' },
                  { label: 'Enterprise SSO',         desc: 'SAML 2.0 / OIDC / Azure AD / Okta' },
                  { label: 'Private Deployment',     desc: 'On-prem or VPC with no data egress' },
                  { label: 'Encryption at Rest',     desc: 'AES-256 for all stored data' },
                ].map(item => (
                  <div key={item.label} className="flex items-start gap-3 p-4 rounded-xl border border-background/10 bg-background/5">
                    <CheckCircle2 className="h-4 w-4 text-background/60 flex-shrink-0 mt-0.5" aria-hidden="true" />
                    <div>
                      <p className="text-caption font-semibold text-background">{item.label}</p>
                      <p className="text-label text-background/50 mt-0.5">{item.desc}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* ── 8. INTEGRATIONS — Will it work with existing HR systems? ──── */}
        <section aria-labelledby="integrations-heading" className="relative border-t border-border">
          <div className="relative max-w-7xl mx-auto px-6 py-16 md:py-20">
            <div className="text-center mb-10 max-w-2xl mx-auto">
              <h2 id="integrations-heading" className="text-heading-lg tracking-tight mb-3">
                Seamless Integration
              </h2>
              <p className="text-body text-muted-foreground">
                Native connectors for the tools your HR teams already use.
              </p>
            </div>
            <div
              className="grid grid-cols-2 md:grid-cols-4 gap-4"
              role="list"
              aria-label="Supported HR integrations"
            >
              {['Workday', 'BambooHR', 'Lattice', 'Slack'].map(name => (
                <div
                  key={name}
                  role="listitem"
                  className="flex items-center justify-center px-6 py-5 rounded-xl border border-border bg-card shadow-sm text-body font-semibold text-muted-foreground hover:text-foreground hover:border-primary/30 motion-safe:transition-all"
                >
                  {name}
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ── 9. MISSION — Why does this company exist? ─────────────────── */}
        <section aria-labelledby="mission-heading" className="relative border-t border-border">
          <div className="absolute inset-0 bg-gradient-to-b from-transparent via-primary/[0.03] to-transparent" aria-hidden="true" />
          <div className="relative max-w-3xl mx-auto px-6 py-16 md:py-24 text-center space-y-6">
            <Target className="h-8 w-8 mx-auto text-primary" aria-hidden="true" />
            <h2 id="mission-heading" className="text-heading-lg tracking-tight">
              Mission & Philosophy
            </h2>
            <p className="text-body-lg text-muted-foreground leading-relaxed">
              We believe every employee deserves an objective, fair, and perfectly calibrated
              evaluation. Our mission is to augment human empathy with algorithmic precision,
              ensuring that the human always owns the final decision, while the machine enforces the standard.
            </p>
          </div>
        </section>

        {/* ── 10. FAQ — Answer buyer objections ────────────────────────── */}
        <section aria-labelledby="faq-heading" className="relative border-t border-border">
          <div className="absolute inset-0 bg-muted/10" aria-hidden="true" />
          <div className="relative max-w-3xl mx-auto px-6 py-16 md:py-20">
            <div className="mb-10 text-center">
              <h2 id="faq-heading" className="text-heading-lg tracking-tight">
                Frequently Asked Questions
              </h2>
            </div>
            <Accordion type="single" collapsible className="w-full" aria-label="Frequently asked questions">
              {FAQ_ITEMS.map((item, i) => (
                <AccordionItem key={i} value={`faq-${i}`}>
                  <AccordionTrigger className="text-body font-medium text-left hover:no-underline py-5">
                    {item.q}
                  </AccordionTrigger>
                  <AccordionContent className="text-body text-muted-foreground leading-relaxed pb-5">
                    {item.a}
                  </AccordionContent>
                </AccordionItem>
              ))}
            </Accordion>
          </div>
        </section>
      </main>

      {/* ── Footer — Where do I go next? ────────────────────────────────── */}
      <footer role="contentinfo" className="border-t border-border bg-card">
        <div className="max-w-7xl mx-auto px-6 py-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-10 pb-10 border-b border-border">
            {/* Brand */}
            <div className="md:col-span-2 space-y-3">
              <div className="flex items-center gap-2">
                <ShieldCheck className="h-5 w-5 text-foreground" aria-hidden="true" />
                <span className="font-bold tracking-tight text-foreground">ReviewGuard AI</span>
              </div>
              <p className="text-caption text-muted-foreground max-w-xs leading-relaxed">
                Eliminating bias in enterprise performance reviews through objective,
                explainable artificial intelligence.
              </p>
            </div>

            {/* Product links */}
            <nav aria-label="Product navigation">
              <p className="text-label font-semibold text-foreground uppercase tracking-wider mb-4">Product</p>
              <ul className="space-y-3 text-caption text-muted-foreground">
                <li>
                  <button
                    id="footer-link-platform"
                    onClick={() => smoothScrollTo('how-it-works')}
                    className="hover:text-foreground motion-safe:transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring rounded-sm"
                  >
                    Platform
                  </button>
                </li>
                <li>
                  <button
                    id="footer-link-security"
                    onClick={() => smoothScrollTo('security')}
                    className="hover:text-foreground motion-safe:transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring rounded-sm"
                  >
                    Security
                  </button>
                </li>
                <li>
                  <a
                    id="footer-link-docs"
                    href="#"
                    className="flex items-center gap-1 hover:text-foreground motion-safe:transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring rounded-sm group"
                    aria-label="Documentation (opens in new tab)"
                  >
                    Documentation
                    <ExternalLink className="h-3 w-3 opacity-50 group-hover:opacity-100 motion-safe:transition-opacity" aria-hidden="true" />
                  </a>
                </li>
              </ul>
            </nav>

            {/* Company links */}
            <nav aria-label="Company navigation">
              <p className="text-label font-semibold text-foreground uppercase tracking-wider mb-4">Company</p>
              <ul className="space-y-3 text-caption text-muted-foreground">
                <li><a id="footer-link-about"   href="#" className="hover:text-foreground motion-safe:transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring rounded-sm">About Us</a></li>
                <li><a id="footer-link-sales"   href="#" className="hover:text-foreground motion-safe:transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring rounded-sm">Contact Sales</a></li>
                <li><a id="footer-link-privacy" href="#" className="hover:text-foreground motion-safe:transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring rounded-sm">Privacy Policy</a></li>
              </ul>
            </nav>
          </div>

          {/* Footer bottom */}
          <div className="flex flex-col md:flex-row items-center justify-between gap-4 pt-8 text-label text-muted-foreground">
            <p>© 2026 ReviewGuard AI Inc. All rights reserved.</p>
            <div className="flex items-center gap-2">
              <div className="h-1.5 w-1.5 rounded-full bg-success" aria-hidden="true" />
              <span role="status" aria-live="polite">All Systems Operational</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
