import { useForm, type SubmitHandler } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { motion } from 'framer-motion';
import { Loader2, AlertCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { PasswordField } from './PasswordField';
import { RememberMe } from './RememberMe';
import { loginSchema } from '../schemas/login.schema';
import type { LoginSchema } from '../schemas/login.schema';
import { useLogin } from '../hooks/useLogin';
import { cn } from '@/lib/utils';

/**
 * LoginForm — production-quality form with:
 *  - React Hook Form + Zod validation
 *  - Real-time field errors
 *  - Show/hide password
 *  - Remember Me
 *  - Loading spinner
 *  - API error alert
 *  - Enter key submits
 *  - Full a11y (labels, aria, focus management)
 */
export function LoginForm() {
  const { login, isLoading, error, isError, reset } = useLogin();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: '',
      password: '',
      rememberMe: false as boolean,
    },
  });

  const onSubmit: SubmitHandler<LoginSchema> = (values) => {
    reset(); // clear previous API error
    login(values);
  };

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      noValidate
      aria-label="Sign in form"
      className="space-y-5"
    >
      {/* ── API Error Alert ── */}
      {isError && error && (
        <motion.div
          role="alert"
          aria-live="assertive"
          initial={{ opacity: 0, y: -4 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-start gap-3 rounded-lg border border-destructive/30 bg-destructive/10 px-4 py-3"
        >
          <AlertCircle className="h-4 w-4 text-destructive mt-0.5 shrink-0" aria-hidden="true" />
          <p className="text-sm text-destructive">
            {error.message ?? 'Invalid credentials. Please try again.'}
          </p>
        </motion.div>
      )}

      {/* ── Email ── */}
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
          className={cn(errors.email && 'border-destructive focus-visible:ring-destructive')}
          {...register('email')}
        />
        {errors.email && (
          <p id="email-error" role="alert" className="text-xs text-destructive">
            {errors.email.message}
          </p>
        )}
      </div>

      {/* ── Password ── */}
      <div className="space-y-1.5">
        <label htmlFor="password" className="block text-sm font-medium text-foreground">
          Password
        </label>
        <PasswordField
          id="password"
          autoComplete="current-password"
          placeholder="••••••••"
          error={errors.password?.message}
          disabled={isLoading}
          {...register('password')}
        />
        {errors.password && (
          <p id="password-error" role="alert" className="text-xs text-destructive">
            {errors.password.message}
          </p>
        )}
      </div>

      {/* ── Remember Me + Forgot Password ── */}
      <div className="flex items-center justify-between">
        <RememberMe
          id="remember-me"
          disabled={isLoading}
          {...register('rememberMe')}
        />
        <button
          type="button"
          className="text-sm text-primary hover:text-primary/80 transition-colors font-medium"
          onClick={() => {
            // Forgot password placeholder — Phase 3
            alert('Password reset will be implemented in Phase 3.');
          }}
        >
          Forgot password?
        </button>
      </div>

      {/* ── Submit Button ── */}
      <Button
        id="login-submit"
        type="submit"
        className="w-full h-11 text-sm font-medium"
        disabled={isLoading}
        aria-disabled={isLoading}
      >
        {isLoading ? (
          <>
            <Loader2 className="mr-2 h-4 w-4 animate-spin" aria-hidden="true" />
            Signing in…
          </>
        ) : (
          'Sign in securely'
        )}
      </Button>
    </form>
  );
}
