import { NavLink } from "react-router-dom";
import { 
  LayoutDashboard, 
  Users, 
  LineChart, 
  FileText, 
  Settings, 
  Target,
  ChevronLeft,
  ChevronRight,
  ShieldCheck
} from "lucide-react";
import { cn } from "@/lib/utils";
import { motion } from "framer-motion";

interface SidebarProps {
  isOpen: boolean;
  setIsOpen: (isOpen: boolean) => void;
}

const navItems = [
  { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { name: "Employees", href: "/employees", icon: Users },
  { name: "Review Cycles", href: "/reviews", icon: Target },
  { name: "AI Insights", href: "/insights", icon: LineChart },
  { name: "Reports", href: "/reports", icon: FileText },
  { name: "Settings", href: "/settings", icon: Settings },
];

export function Sidebar({ isOpen, setIsOpen }: SidebarProps) {
  return (
    <motion.aside
      initial={false}
      animate={{ width: isOpen ? 260 : 72 }}
      className="bg-card border-r border-border h-screen flex flex-col relative z-20 shrink-0"
    >
      <div className="h-16 flex items-center px-4 border-b border-border">
        <ShieldCheck className="h-8 w-8 text-brand-blue shrink-0" />
        {isOpen && (
          <motion.span 
            initial={{ opacity: 0 }} 
            animate={{ opacity: 1 }} 
            className="ml-3 font-semibold text-lg whitespace-nowrap tracking-tight"
          >
            ReviewGuard <span className="text-brand-blue">AI</span>
          </motion.span>
        )}
      </div>

      <div className="flex-1 overflow-y-auto py-6 px-3 space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.href}
              to={item.href}
              className={({ isActive }) =>
                cn(
                  "flex items-center px-3 py-2.5 rounded-md transition-colors group",
                  isActive 
                    ? "bg-primary/10 text-brand-blue font-medium" 
                    : "text-muted-foreground hover:bg-muted hover:text-foreground"
                )
              }
              title={!isOpen ? item.name : undefined}
            >
              <Icon className="h-5 w-5 shrink-0" />
              {isOpen && (
                <span className="ml-3 truncate">{item.name}</span>
              )}
            </NavLink>
          );
        })}
      </div>

      <div className="p-3 border-t border-border">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="flex w-full items-center justify-center p-2 rounded-md text-muted-foreground hover:bg-muted hover:text-foreground transition-colors"
        >
          {isOpen ? <ChevronLeft className="h-5 w-5" /> : <ChevronRight className="h-5 w-5" />}
        </button>
      </div>
    </motion.aside>
  );
}
