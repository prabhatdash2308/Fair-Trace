import * as React from "react"
import { cn } from "@/lib/utils"

/**
 * Input — normalized to design system.
 * Height: h-9 (36px) — consistent across all forms.
 * Radius: rounded-md (8px).
 * Focus: ring-2 ring-ring/50 with no offset (cleaner on dark bg).
 * Transition: 120ms colors.
 */
export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(
          // Layout
          "flex h-9 w-full px-3 py-1.5",
          // Typography
          "text-body text-foreground placeholder:text-muted-foreground/60",
          // Styling
          "rounded-md border border-input bg-background",
          // File input
          "file:border-0 file:bg-transparent file:text-sm file:font-medium",
          // Focus
          "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring/50 focus-visible:border-ring/60",
          // States
          "disabled:cursor-not-allowed disabled:opacity-50 disabled:bg-muted/50",
          "read-only:bg-muted/30 read-only:cursor-default",
          // Transition
          "transition-colors duration-[120ms]",
          className
        )}
        ref={ref}
        {...props}
      />
    )
  }
)
Input.displayName = "Input"

export { Input }
