import { useNavigate } from 'react-router-dom';
import { ShieldOff, ArrowLeft } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useAuthStore } from '@/store/auth/auth.store';
import { roleDashboardRoute } from '@/constants/routes';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';

/**
 * UnauthorizedPage — 403 page rendered when a user attempts to access
 * a dashboard workspace that does not match their role.
 */
export function UnauthorizedPage() {
  useDocumentTitle('Unauthorized — FairTrace');
  const navigate = useNavigate();
  const { user } = useAuthStore();

  const destination = roleDashboardRoute(user?.role);

  return (
    <div className="min-h-screen bg-background flex items-center justify-center px-6">
      <div className="max-w-md w-full text-center space-y-6">
        <div className="flex items-center justify-center w-16 h-16 rounded-2xl bg-danger/10 border border-danger/20 mx-auto">
          <ShieldOff className="h-8 w-8 text-danger" aria-hidden="true" />
        </div>

        <div className="space-y-2">
          <p className="text-label font-semibold text-danger uppercase tracking-widest">
            403 — Unauthorized
          </p>
          <h1 className="text-heading-lg tracking-tight text-foreground">
            Access Denied
          </h1>
          <p className="text-body text-muted-foreground leading-relaxed">
            You don&apos;t have permission to access this workspace.
            {user?.role && (
              <> Your account is assigned to the{' '}
                <span className="font-medium text-foreground">
                  {user.role.charAt(0) + user.role.slice(1).toLowerCase()}
                </span>{' '}
                workspace.
              </>
            )}
          </p>
        </div>

        <div className="flex flex-col sm:flex-row gap-3 justify-center">
          <Button
            id="btn-go-workspace"
            onClick={() => navigate(destination, { replace: true })}
          >
            Go to My Workspace
          </Button>
          <Button
            id="btn-go-back"
            variant="outline"
            onClick={() => navigate(-1)}
            className="gap-2"
          >
            <ArrowLeft className="h-4 w-4" aria-hidden="true" />
            Go Back
          </Button>
        </div>

        <p className="text-caption text-muted-foreground">
          If you believe this is an error, contact your system administrator.
        </p>
      </div>
    </div>
  );
}
