# ReviewGuard AI — Enterprise Design System (Phase 3.5 Foundation)

This document outlines the core design system for ReviewGuard AI. The system is intentionally built incrementally ("Extract as we build"). The foundation layers described here represent the shared primitives that all future complex components will consume.

## Design Philosophy

The design language is inspired by Vercel, Linear, and Stripe. It prioritizes:
- **Professionalism:** Minimalist, data-dense, and clean.
- **Subtlety:** Avoiding neon colors, heavy gradients, or excessive animations.
- **Consistency:** Centralized tokens and rigorous component reuse.
- **Accessibility:** High contrast, clear focus states, and semantic HTML.

## 1. Tokens (`src/theme/`)

The tokens define the strict visual boundaries of the application.

- **Colors:** Defined in `globals.css` as CSS variables, mapped in `tailwind.config.js`, and typed in `src/theme/colors.ts`. Never use magic hex codes in components.
- **Spacing:** Extended spacing scale (`32`, `40`, `48`, `64`) added to `tokens.ts` and Tailwind config for layout grids.
- **Shadows:** `sm`, `md`, `lg`, `xl`, `2xl`, plus semantic shadows `floating` and `glass`.
- **Transitions:** Standardized transition curves (`default`, `fast`, `slow`).

## 2. Icons (`src/components/icons/`)

All icons are imported exclusively from `lucide-react` via centralized domain exports. This ensures consistent icon choices across the app.

- `NavIcons`: `navigation.ts` (Dashboard, Employees, Search, Menu)
- `ActionIcons`: `actions.ts` (Add, Edit, Delete, Confirm, Cancel)
- `StatusIcons`: `status.ts` (Success, Error, Warning, Info, Pending)
- `AIIcons`: `ai.ts` (Sparkles, Bot, Brain, Explain)
- `FileIcons`: `file.ts` (PDF, CSV, Upload, Download, Attachment)

## 3. Motion (`src/components/motion/`)

All animations use `framer-motion`. Magic animation configurations are forbidden in individual components.
Use the centralized variants from `variants.ts`:
- `fadeVariants`
- `slideUpVariants`
- `scaleVariants`
- `staggerContainer`
- `pageTransition`

## 4. Component Layers

### Shadcn UI Primitives (`src/components/ui/`)
The base layer of interactivity. We use shadcn for Inputs, Tooltips, Separators, etc. 
- **Buttons:** We enforce semantic wrappers (`PrimaryButton`, `SecondaryButton`, `DangerButton`, `LoadingButton`, `IconButton`) over the raw shadcn `<Button>` to guarantee consistent sizing, variants, and active states.

### Forms (`src/components/forms/`)
Reusable form inputs that compose shadcn primitives with labels, hints, and error states.
- `TextField`, `SearchField`, `CheckboxField`, `SwitchField`, `PasswordField`

### Status & Feedback (`src/components/status/`, `src/components/feedback/`)
Semantic indicators.
- **Status:** `StatusBadge`, `ApprovalStatus`, `PipelineStatus`, `ReviewStatus`, `ConfidenceBadge`.
- **Feedback:** `LoadingTable`, `PermissionDenied`, `RetryCard`, `SuccessBanner`, `EmptyStates`.

### Layout (`src/components/layout/`)
Structural containers enforcing consistent spacing and grid alignments.
- `ResponsiveGrid`, `DashboardGrid`, `PageToolbar`, `ActionBar`, `PageSection`, `StatGrid`.

## 5. Do's and Don'ts

### Do
- Always use the semantic button wrappers (`PrimaryButton`, etc.) instead of `<Button variant="...">`.
- Always import icons from `@/components/icons` instead of `lucide-react` directly.
- Use `ResponsiveGrid` or `DashboardGrid` for structural layouts instead of writing custom grid classes.
- Ensure all interactive elements have focus rings (handled by global `focus-visible` styles).

### Don't
- Do not migrate to Tailwind v4. We extend the existing v3 config.
- Do not add new UI libraries (Material UI, Chakra, etc.).
- Do not add arbitrary Framer Motion transition objects to components. Use `src/components/motion/variants.ts`.

## 6. Future Component Extraction Strategy

As we move into feature development (e.g., Phase 4 Dashboard), we will encounter the need for complex organisms:
- `Charts` (Recharts wrappers)
- `Tables` (Data grids, pagination, toolbars)
- `Cards` (MetricCard, InfoCard)
- `AI` (EvidenceTimeline, ReasoningTimeline)

**Rule:** We will NOT build these preemptively. They will be created inside `src/components/charts/`, `src/components/tables/`, etc., *only* when the feature being built actively requires them. This ensures every component is grounded in a real product requirement.
