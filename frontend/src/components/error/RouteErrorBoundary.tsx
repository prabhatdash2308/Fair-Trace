import { useRouteError, isRouteErrorResponse } from 'react-router-dom';
import { AlertOctagon, WifiOff, FileQuestion, ArrowLeft } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useNavigate } from 'react-router-dom';

export function RouteErrorBoundary() {
  const error = useRouteError();
  const navigate = useNavigate();
  
  let title = "Unexpected Error";
  let message = "An error occurred while loading this module.";
  let Icon = AlertOctagon;
  let showRetry = true;

  if (isRouteErrorResponse(error)) {
    if (error.status === 404) {
      title = "Module Not Found";
      message = "The requested resource or page does not exist.";
      Icon = FileQuestion;
      showRetry = false;
    } else if (error.status === 500) {
      title = "Server Error";
      message = "The ReviewGuard AI engine is currently experiencing issues. Please try again.";
      Icon = AlertOctagon;
    } else if (error.status === 503) {
      title = "Service Unavailable";
      message = "We are performing routine maintenance. We'll be back shortly.";
      Icon = WifiOff;
    }
  } else if (error instanceof TypeError && error.message.includes('fetch')) {
    title = "Network Failure";
    message = "Unable to connect to ReviewGuard AI services. Please check your internet connection.";
    Icon = WifiOff;
  }

  return (
    <div className="flex-1 flex flex-col items-center justify-center min-h-[60vh] text-center px-4">
      <div className="h-16 w-16 bg-muted rounded-2xl flex items-center justify-center mb-6">
        <Icon className="h-8 w-8 text-muted-foreground" />
      </div>
      <h2 className="text-2xl font-semibold tracking-tight mb-2">{title}</h2>
      <p className="text-muted-foreground max-w-md mb-8">{message}</p>
      
      <div className="flex items-center gap-4">
        {showRetry && (
          <Button onClick={() => window.location.reload()}>
            Retry Connection
          </Button>
        )}
        <Button variant={showRetry ? "outline" : "default"} onClick={() => navigate(-1)} className="gap-2">
          <ArrowLeft className="h-4 w-4" />
          Go Back
        </Button>
      </div>
    </div>
  );
}
