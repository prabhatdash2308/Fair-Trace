import { Link } from 'react-router-dom';
import { FileQuestion, ArrowLeft } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { ROUTES } from '@/constants/routes';

export function NotFoundPage() {
  return (
    <div className="min-h-screen bg-background flex flex-col items-center justify-center px-4 text-center">
      <div className="h-16 w-16 bg-muted rounded-2xl flex items-center justify-center mb-6">
        <FileQuestion className="h-8 w-8 text-muted-foreground" />
      </div>
      <h1 className="text-3xl font-semibold tracking-tight mb-2">404 — Page Not Found</h1>
      <p className="text-muted-foreground max-w-md mb-8">
        The requested resource does not exist or you do not have permission to access it.
      </p>
      <Link to={ROUTES.DASHBOARD}>
        <Button className="gap-2">
          <ArrowLeft className="h-4 w-4" />
          Return to Dashboard
        </Button>
      </Link>
    </div>
  );
}
