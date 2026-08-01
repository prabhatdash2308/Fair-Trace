import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { ShieldCheck, BarChart3, Users, Zap, CheckCircle2 } from "lucide-react";
import { motion } from "framer-motion";

export function LandingPage() {
  return (
    <div className="min-h-screen bg-background flex flex-col font-sans">
      {/* Navbar */}
      <header className="container mx-auto px-6 h-20 flex items-center justify-between border-b border-border">
        <div className="flex items-center space-x-2">
          <ShieldCheck className="h-8 w-8 text-brand-blue" />
          <span className="text-xl font-bold tracking-tight">
            ReviewGuard <span className="text-brand-blue">AI</span>
          </span>
        </div>
        <div className="flex items-center space-x-6">
          <nav className="hidden md:flex space-x-8 text-sm font-medium text-muted-foreground">
            <a href="#features" className="hover:text-foreground transition-colors">Features</a>
            <a href="#security" className="hover:text-foreground transition-colors">Security</a>
            <a href="#pricing" className="hover:text-foreground transition-colors">Pricing</a>
          </nav>
          <div className="flex items-center space-x-4">
            <Link to="/login" className="text-sm font-medium hover:text-brand-blue transition-colors">
              Sign In
            </Link>
            <Link to="/login">
              <Button>Get Started</Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="flex-1 flex flex-col items-center justify-center text-center px-6 py-24">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="max-w-4xl mx-auto space-y-8"
        >
          <div className="inline-flex items-center rounded-full border border-border px-3 py-1 text-sm bg-muted/50 text-muted-foreground mb-4">
            <Zap className="mr-2 h-4 w-4 text-warning-orange" />
            <span>Introducing Predictive Performance AI</span>
          </div>
          
          <h1 className="text-5xl md:text-7xl font-bold tracking-tight text-foreground leading-[1.1]">
            Enterprise performance reviews, <br/>
            <span className="text-brand-blue">engineered for precision.</span>
          </h1>
          
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
            ReviewGuard AI eliminates bias and standardizes evaluations across your entire organization with intelligence you can trust. Built for the modern Fortune 500.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4 pt-8">
            <Link to="/dashboard">
              <Button size="lg" className="w-full sm:w-auto h-12 px-8 text-base">
                View Dashboard Demo
              </Button>
            </Link>
            <Button size="lg" variant="outline" className="w-full sm:w-auto h-12 px-8 text-base">
              Contact Sales
            </Button>
          </div>
          
          <div className="pt-12 text-sm text-muted-foreground flex items-center justify-center space-x-8 opacity-70">
            <div className="flex items-center"><CheckCircle2 className="mr-2 h-4 w-4" /> SOC2 Compliant</div>
            <div className="flex items-center"><CheckCircle2 className="mr-2 h-4 w-4" /> SSO Integration</div>
            <div className="flex items-center"><CheckCircle2 className="mr-2 h-4 w-4" /> 99.99% Uptime</div>
          </div>
        </motion.div>
        
        {/* Placeholder for Dashboard Preview */}
        <motion.div 
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.2 }}
          className="mt-24 w-full max-w-6xl rounded-xl border border-border bg-card shadow-2xl overflow-hidden aspect-[16/9] relative flex items-center justify-center"
        >
          <div className="absolute inset-0 bg-gradient-to-b from-transparent to-background/20" />
          <div className="text-muted-foreground flex flex-col items-center">
            <BarChart3 className="h-16 w-16 mb-4 opacity-50" />
            <p className="font-medium text-lg">Interactive Dashboard Preview</p>
          </div>
        </motion.div>
      </main>

      {/* Footer */}
      <footer className="border-t border-border py-12 text-center text-sm text-muted-foreground">
        <p>© 2026 ReviewGuard AI. All rights reserved.</p>
      </footer>
    </div>
  );
}
