/**
 * RoleSelector.tsx — Enterprise workspace role selection cards.
 *
 * Polished:
 * - Center aligned.
 * - Equal width.
 * - Smooth 150ms transitions (no bounce).
 */
import * as React from 'react';
import { motion } from 'framer-motion';
import { Shield, Users, User } from 'lucide-react';
import { cn } from '@/lib/utils';
import type { Role } from '@/constants/roles';

interface RoleSelectorProps {
  selectedRole: Role | null;
  onSelect: (role: Role) => void;
}

const ROLE_CARDS = [
  {
    role: 'ADMIN' as Role,
    icon: Shield,
    title: 'Administrator',
    description: 'Platform Settings',
  },
  {
    role: 'MANAGER' as Role,
    icon: Users,
    title: 'Manager',
    description: 'Team Performance',
  },
  {
    role: 'EMPLOYEE' as Role,
    icon: User,
    title: 'Employee',
    description: 'Personal Workspace',
  },
] as const;

export function RoleSelector({ selectedRole, onSelect }: RoleSelectorProps) {
  return (
    <div role="group" aria-label="Choose your workspace" className="flex gap-2">
      {ROLE_CARDS.map((card) => {
        const Icon = card.icon;
        const isSelected = selectedRole === card.role;

        return (
          <button
            key={card.role}
            type="button"
            role="radio"
            aria-checked={isSelected}
            aria-label={`${card.title} workspace: ${card.description}`}
            onClick={() => onSelect(card.role)}
            className={cn(
              'relative flex-1 flex flex-col items-center justify-center py-4 px-2 text-center rounded-[14px] border transition-all duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
              isSelected
                ? 'border-primary bg-primary/10 shadow-[0_0_15px_rgba(var(--primary),0.15)]'
                : 'border-border/60 bg-background hover:border-border hover:bg-muted/30'
            )}
          >
            {/* Selection indicator */}
            {isSelected && (
              <motion.div
                layoutId="role-selector-active"
                className="absolute inset-0 rounded-[14px] border border-primary pointer-events-none"
                initial={false}
                transition={{ duration: 0.15, ease: 'easeOut' }}
              />
            )}
            
            <Icon 
              className={cn(
                'h-5 w-5 mb-1.5 transition-colors duration-150',
                isSelected ? 'text-primary' : 'text-muted-foreground'
              )} 
              aria-hidden="true" 
            />
            <span className={cn(
              'text-[13px] font-semibold mb-0.5 transition-colors duration-150 tracking-tight',
              isSelected ? 'text-foreground' : 'text-muted-foreground'
            )}>
              {card.title}
            </span>
            <span className="text-[10px] leading-tight text-muted-foreground/80 font-medium">
              {card.description}
            </span>
          </button>
        );
      })}
    </div>
  );
}
