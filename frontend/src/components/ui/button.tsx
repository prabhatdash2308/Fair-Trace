import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

/**
 * Button — normalized to design system.
 * All sizes are consistent height tokens. No ad-hoc sizing.
 * Consistent border-radius: rounded-md (8px).
 * Transitions: 120ms (fast) for interactive feel.
 */
const buttonVariants = cva(
  [
    "inline-flex items-center justify-center gap-2 font-medium whitespace-nowrap",
    "rounded-md transition-colors select-none",
    "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring/60 focus-visible:ring-offset-2 focus-visible:ring-offset-background",
    "disabled:pointer-events-none disabled:opacity-40",
    "[&_svg]:pointer-events-none [&_svg]:shrink-0",
  ].join(" "),
  {
    variants: {
      variant: {
        // Primary — blue, for main CTAs only
        default:
          "bg-primary text-primary-foreground shadow-sm hover:bg-primary/90 active:bg-primary/80",
        // Destructive — for dangerous irreversible actions
        destructive:
          "bg-danger text-danger-foreground shadow-sm hover:bg-danger/90 active:bg-danger/80",
        // Outline — secondary actions
        outline:
          "border border-border bg-background text-foreground hover:bg-muted/70 hover:border-border/80 active:bg-muted",
        // Secondary — muted surface
        secondary:
          "bg-secondary text-secondary-foreground hover:bg-secondary/70 active:bg-secondary/60",
        // Ghost — lowest emphasis, for icon buttons and nav actions
        ghost:
          "text-muted-foreground hover:bg-muted hover:text-foreground active:bg-muted/80",
        // Link — inline text action
        link:
          "text-primary underline-offset-4 hover:underline p-0 h-auto",
      },
      size: {
        // All non-link buttons have normalized heights
        xs:      "h-7 px-2.5 text-[11px] rounded",
        sm:      "h-8 px-3 text-xs",
        default: "h-10 px-4 text-sm",
        lg:      "h-11 px-5 text-sm",
        xl:      "h-12 px-6 text-base",
        // Icon sizes — square
        icon:    "h-10 w-10",
        "icon-sm": "h-8 w-8",
        "icon-xs": "h-7 w-7",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
  loading?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, loading, children, disabled, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        disabled={disabled || loading}
        aria-disabled={disabled || loading}
        {...props}
      >
        {loading ? (
          <>
            <svg
              className="h-4 w-4 animate-spin-slow opacity-70"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
            {children}
          </>
        ) : (
          children
        )}
      </Comp>
    )
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }
