import * as React from 'react';
import { cn } from '@/lib/utils';
import type { LucideIcon } from 'lucide-react';

export interface TimelineEvent {
  id: string;
  title: string;
  description?: React.ReactNode;
  date: string;
  icon?: LucideIcon;
  iconColor?: string; // e.g. 'text-blue-500'
  iconBg?: string;    // e.g. 'bg-blue-500/10'
  isActive?: boolean;
}

export interface TimelineProps {
  events: TimelineEvent[];
  className?: string;
}

export const Timeline: React.FC<TimelineProps> = ({ events, className }) => {
  if (!events?.length) return null;

  return (
    <div className={cn('relative space-y-4 before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-border before:to-transparent', className)}>
      {events.map((event, index) => {
        const Icon = event.icon;
        return (
          <div key={event.id} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
            {/* Icon */}
            <div className={cn(
              'flex items-center justify-center w-10 h-10 rounded-full border-4 border-background shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 shadow-sm',
              event.isActive ? 'bg-primary text-primary-foreground' : event.iconBg || 'bg-muted'
            )}>
              {Icon && <Icon className={cn('w-4 h-4', event.isActive ? 'text-primary-foreground' : event.iconColor || 'text-muted-foreground')} />}
            </div>
            
            {/* Card */}
            <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-4 rounded-lg border border-border/50 bg-card shadow-sm hover:shadow-floating transition-shadow">
              <div className="flex items-center justify-between mb-1">
                <h4 className="text-sm font-semibold text-foreground">{event.title}</h4>
                <time className="text-xs text-muted-foreground font-mono">{event.date}</time>
              </div>
              {event.description && (
                <div className="text-sm text-muted-foreground mt-2">
                  {event.description}
                </div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};
