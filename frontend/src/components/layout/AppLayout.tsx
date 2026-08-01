import { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { Header } from './Header';
import { Footer } from './Footer';
import { Breadcrumbs } from './Breadcrumbs';

/**
 * AppLayout — the authenticated application shell.
 *
 * Structure:
 *   ┌─────────────────────────────────────────┐
 *   │  Header (top navigation bar)            │
 *   ├─────────┬───────────────────────────────┤
 *   │ Sidebar │  Breadcrumbs                  │
 *   │         │  ────────────────────────     │
 *   │         │  <Outlet /> (page content)    │
 *   │         │                               │
 *   │         │  Footer                       │
 *   └─────────┴───────────────────────────────┘
 */
export function AppLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col overflow-hidden">
      {/* Top Navigation */}
      <Header sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />

      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        <Sidebar isOpen={sidebarOpen} setIsOpen={setSidebarOpen} />

        {/* Content area */}
        <div className="flex flex-col flex-1 min-w-0 overflow-hidden">
          <main
            id="main-content"
            className="flex-1 overflow-y-auto focus:outline-none"
            tabIndex={-1}
          >
            <div className="max-w-7xl mx-auto px-6 py-6">
              {/* Breadcrumbs */}
              <Breadcrumbs />

              {/* Page outlet */}
              <Outlet />
            </div>
          </main>

          {/* Footer */}
          <Footer />
        </div>
      </div>
    </div>
  );
}
