import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

/**
 * Badge — enterprise status chips.
 * Uses rounded-md (8px) NOT rounded-full for status badges.
 * Subtle backgrounds — never saturated colors.
 * Consistent height and padding across all variants.
 */
const badgeVariants = cva(
  [
    "inline-flex items-center gap-1 rounded-md border px-2 py-0.5",
    "text-[11px] font-medium leading-none",
    "transition-colors duration-[120ms]",
    "focus:outline-none focus:ring-2 focus:ring-ring/50 focus:ring-offset-1",
    "select-none whitespace-nowrap",
  ].join(" "),
  {
    variants: {
      variant: {
        // Primary — for active/highlighted states
        default:
          "border-primary/20 bg-primary/10 text-primary",
        // Neutral — for secondary/inactive
        secondary:
          "border-border bg-muted text-muted-foreground",
        // Destructive — danger/error
        destructive:
          "border-danger/20 bg-danger/10 text-danger",
        // Outline — no fill, just border
        outline:
          "border-border text-foreground bg-transparent",
        // Success — completed/healthy
        success:
          "border-success/20 bg-success/10 text-success",
        // Warning — attention needed
        warning:
          "border-warning/20 bg-warning/10 text-warning",
        // Info — informational
        info:
          "border-info/20 bg-info/10 text-info",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

export interface BadgeProps
  extends React.HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <span className={cn(badgeVariants({ variant }), className)} {...props} />
  )
}

export { Badge, badgeVariants }
