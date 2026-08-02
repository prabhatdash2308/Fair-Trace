import { useForm, type SubmitHandler } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { motion } from 'framer-motion';
import { Loader2, AlertCircle, Check } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { PasswordField } from './PasswordField';
import { RememberMe } from './RememberMe';
import { loginSchema } from '../schemas/login.schema';
import type { LoginSchema } from '../schemas/login.schema';
import { useLogin } from '../hooks/useLogin';
import { Link } from 'react-router-dom';
import { cn } from '@/lib/utils';
import { ROUTES } from '@/constants/routes';

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
      className="space-y-4 w-full"
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
          className={cn('h-11', errors.email && 'border-destructive focus-visible:ring-destructive')}
          {...register('email')}
        />
        {errors.email && (
          <p id="email-error" role="alert" className="text-[13px] text-destructive">
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
          className="h-11"
          {...register('password')}
        />
        {errors.password && (
          <p id="password-error" role="alert" className="text-[13px] text-destructive">
            {errors.password.message}
          </p>
        )}
      </div>

      {/* ── Remember Me + Forgot Password ── */}
      <div className="flex items-center justify-between pt-1 pb-1">
        <RememberMe
          id="remember-me"
          disabled={isLoading}
          {...register('rememberMe')}
        />
        <Link
          to={ROUTES.FORGOT_PASSWORD}
          className="text-[13px] text-primary hover:text-primary/80 transition-colors font-semibold"
        >
          Forgot password?
        </Link>
      </div>

      {/* ── Submit Button ── */}
      <Button
        id="login-submit"
        type="submit"
        className={cn(
          "w-full h-11 text-[15px] font-semibold transition-all duration-100",
          "bg-gradient-to-b from-primary/90 to-primary shadow-[0_1px_2px_rgba(0,0,0,0.1),0_0_0_1px_rgba(var(--primary),0.5)_inset]",
          "hover:shadow-[0_4px_12px_rgba(var(--primary),0.25),0_0_0_1px_rgba(var(--primary),0.8)_inset] hover:-translate-y-[0.5px]",
          "active:shadow-none active:translate-y-[0.5px]"
        )}
        disabled={isLoading}
        aria-disabled={isLoading}
      >
        {isLoading ? (
          <div className="flex items-center gap-2">
            <Loader2 className="h-4 w-4 animate-spin opacity-70" aria-hidden="true" />
            Signing in...
          </div>
        ) : (
          'Sign in securely'
        )}
      </Button>
    </form>
  );
}
