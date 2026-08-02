import { useState } from 'react';
import { useForm, type SubmitHandler } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { motion } from 'framer-motion';
import { Loader2, ShieldCheck, ArrowLeft, MailCheck } from 'lucide-react';
import { Link } from 'react-router-dom';
import { GlassCard } from '@/components/cult/GlassCard';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useToast } from '@/components/ui/use-toast';
import { APP_CAPABILITIES } from '@/config/capabilities';
import { ROUTES } from '@/constants/routes';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';

const forgotPasswordSchema = z.object({
  email: z.string().email('Please enter a valid corporate email address.'),
});

type ForgotPasswordSchema = z.infer<typeof forgotPasswordSchema>;

export function ForgotPasswordPage() {
  useDocumentTitle('Reset Password');
  const { toast } = useToast();
  const [isLoading, setIsLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ForgotPasswordSchema>({
    resolver: zodResolver(forgotPasswordSchema),
    defaultValues: { email: '' },
  });

  const onSubmit: SubmitHandler<ForgotPasswordSchema> = async (values) => {
    setIsLoading(true);

    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 800));
    setIsLoading(false);

    if (!APP_CAPABILITIES.auth.forgotPassword) {
      toast({
        variant: 'destructive',
        title: 'Action Unavailable',
        description: 'Password reset is not enabled for your organization.',
      });
      return;
    }

    // Real action if it was enabled
    setIsSuccess(true);
  };

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
          {!isSuccess ? (
            <>
              {/* ── Brand header ── */}
              <div className="flex flex-col items-center mb-8">
                <div className="flex items-center justify-center h-12 w-12 rounded-xl bg-primary/10 mb-4">
                  <ShieldCheck className="h-6 w-6 text-primary" aria-hidden="true" />
                </div>
                <h1 className="text-2xl font-bold text-foreground tracking-tight">
                  Reset Password
                </h1>
                <p className="mt-1 text-sm text-muted-foreground text-center">
                  Enter your email address and we will send you instructions to reset your password.
                </p>
              </div>

              {/* ── Forgot Password form ── */}
              <form onSubmit={handleSubmit(onSubmit)} noValidate className="space-y-5">
                <div className="space-y-1.5">
                  <label htmlFor="email" className="block text-sm font-medium text-foreground">
                    Corporate Email
                  </label>
                  <Input
                    id="email"
                    type="email"
                    autoComplete="email"
                    autoFocus
                    placeholder="name@company.com"
                    aria-describedby={errors.email ? 'email-error' : undefined}
                    aria-invalid={!!errors.email}
                    disabled={isLoading}
                    className={errors.email ? 'border-destructive focus-visible:ring-destructive' : ''}
                    {...register('email')}
                  />
                  {errors.email && (
                    <p id="email-error" role="alert" className="text-xs text-destructive">
                      {errors.email.message}
                    </p>
                  )}
                </div>

                <Button
                  type="submit"
                  className="w-full h-11 text-sm font-medium"
                  disabled={isLoading}
                  aria-disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" aria-hidden="true" />
                      Sending Instructions…
                    </>
                  ) : (
                    'Send Reset Instructions'
                  )}
                </Button>
              </form>
            </>
          ) : (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="flex flex-col items-center text-center py-4"
            >
              <div className="flex items-center justify-center h-12 w-12 rounded-full bg-success/20 mb-4 text-success">
                <MailCheck className="h-6 w-6" />
              </div>
              <h2 className="text-2xl font-semibold tracking-tight mb-2">Check your email</h2>
              <p className="text-muted-foreground text-sm mb-6">
                We sent a password reset link to your email address. Please click the link to continue.
              </p>
            </motion.div>
          )}

          {/* ── Footer link ── */}
          <p className="mt-6 text-center text-xs text-muted-foreground">
            <Link
              to={ROUTES.LOGIN}
              className="inline-flex items-center hover:text-foreground transition-colors font-medium"
            >
              <ArrowLeft className="mr-2 h-3.5 w-3.5" />
              Return to sign in
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

