import * as React from 'react';
import { FileQuestion } from 'lucide-react';
import { PrimaryButton } from '@/components/ui/PrimaryButton';
import { useNavigate } from 'react-router-dom';

interface NotFoundProps {
  title?: string;
  message?: string;
  showHomeButton?: boolean;
}

export const NotFound: React.FC<NotFoundProps> = ({
  title = 'Page Not Found',
  message = "The page you're looking for doesn't exist or has been moved.",
  showHomeButton = true,
}) => {
  const navigate = useNavigate();

  return (
    <div className="flex min-h-[400px] flex-col items-center justify-center space-y-4 text-center">
      <div className="flex h-16 w-16 items-center justify-center rounded-full bg-muted">
        <FileQuestion className="h-8 w-8 text-muted-foreground" />
      </div>
      <div className="space-y-2">
        <h2 className="text-2xl font-semibold tracking-tight">{title}</h2>
        <p className="text-sm text-muted-foreground">{message}</p>
      </div>
      {showHomeButton && (
        <PrimaryButton onClick={() => navigate('/')} variant="default">
          Return Home
        </PrimaryButton>
      )}
    </div>
  );
};
