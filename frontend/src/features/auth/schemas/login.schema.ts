import { z } from 'zod';

/**
 * Zod schema for the login form.
 * Single source of truth for validation — used by React Hook Form resolver.
 */
export const loginSchema = z.object({
  email: z
    .string()
    .min(1, 'Email is required')
    .email('Please enter a valid email address'),

  password: z
    .string()
    .min(1, 'Password is required')
    .min(6, 'Password must be at least 6 characters'),

  rememberMe: z.boolean(),
});

export type LoginSchema = z.infer<typeof loginSchema>;
