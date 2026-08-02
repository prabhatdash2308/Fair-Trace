import { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { Header } from './Header';
import { Footer } from './Footer';

/**
 * AppLayout — authenticated application shell.
 *
 * Structure:
 *   ┌───────────────────────────────────────────┐
 *   │  Header (sticky, h-14)                    │
 *   ├────────┬──────────────────────────────────┤
 *   │Sidebar │  <Outlet /> (page content)        │
 *   │(240px) │  px-8 py-8 max-w-screen-xl        │
 *   │        │                                   │
 *   │        │  Footer                           │
 *   └────────┴──────────────────────────────────┘
 */
export function AppLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col overflow-hidden">
      {/* Sticky top navigation */}
      <Header sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />

      <div className="flex flex-1 overflow-hidden">
        {/* Side navigation */}
        <Sidebar isOpen={sidebarOpen} setIsOpen={setSidebarOpen} />

        {/* Content area */}
        <div className="flex flex-col flex-1 min-w-0 overflow-hidden">
          <main
            id="main-content"
            className="flex-1 overflow-y-auto focus:outline-none scrollbar-thin"
            tabIndex={-1}
          >
            {/* Consistent page padding — strict 8px grid */}
            <div className="max-w-screen-xl mx-auto px-8 py-8">
              <Outlet />
            </div>
          </main>

          <Footer />
        </div>
      </div>
    </div>
  );
}
