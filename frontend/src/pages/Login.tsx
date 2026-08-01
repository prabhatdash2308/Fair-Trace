import { LoginCard } from '@/features/auth';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';

/**
 * Login page — thin orchestration wrapper.
 * All logic lives in the auth feature module.
 * LoginCard handles: form, validation, API, animation, layout.
 */
export function Login() {
  useDocumentTitle('Sign In');

  return <LoginCard />;
}
