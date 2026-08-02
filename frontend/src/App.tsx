import { Suspense, lazy } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AppLayout } from '@/components/layout/AppLayout';
import { ProtectedRoute } from '@/guards/ProtectedRoute';
import { GuestRoute } from '@/guards/GuestRoute';
import { DashboardRoleGuard } from '@/guards/DashboardRoleGuard';
import { ROUTES } from '@/constants/routes';
import { Loader2 } from 'lucide-react';

// Lazy-loaded routes
const LandingPage = lazy(() => import('@/pages/LandingPage').then(m => ({ default: m.LandingPage })));
const Login = lazy(() => import('@/pages/Login').then(m => ({ default: m.Login })));
const NotFoundPage = lazy(() => import('@/pages/NotFoundPage').then(m => ({ default: m.NotFoundPage })));
const ForgotPasswordPage = lazy(() => import('@/pages/ForgotPasswordPage').then(m => ({ default: m.ForgotPasswordPage })));
const RoleDashboardRedirect = lazy(() => import('@/pages/RoleDashboardRedirect').then(m => ({ default: m.RoleDashboardRedirect })));
const AdminDashboard = lazy(() => import('@/pages/dashboards/AdminDashboard').then(m => ({ default: m.AdminDashboard })));
const ManagerDashboard = lazy(() => import('@/pages/dashboards/ManagerDashboard').then(m => ({ default: m.ManagerDashboard })));
const EmployeeDashboard = lazy(() => import('@/pages/dashboards/EmployeeDashboard').then(m => ({ default: m.EmployeeDashboard })));
const UnauthorizedPage = lazy(() => import('@/pages/UnauthorizedPage').then(m => ({ default: m.UnauthorizedPage })));
const EmployeesPage = lazy(() => import('@/pages/EmployeesPage'));
const EmployeeDetailsPage = lazy(() => import('@/pages/EmployeeDetailsPage'));
const PipelinePage = lazy(() => import('@/pages/PipelinePage'));
const PipelineHistoryPage = lazy(() => import('@/pages/PipelineHistoryPage'));
const PipelineRunPage = lazy(() => import('@/pages/PipelineRunPage'));
const ReviewsPage = lazy(() => import('@/pages/ReviewsPage'));
const ReviewDetailsPage = lazy(() => import('@/pages/ReviewDetailsPage'));
const ReportsPage = lazy(() => import('@/pages/ReportsPage'));
const ReportDetailsPage = lazy(() => import('@/pages/ReportDetailsPage'));
const ExplainabilityDetailsPage = lazy(() => import('@/pages/ExplainabilityDetailsPage'));
const AIInsights = lazy(() => import('@/pages/AIInsights').then(m => ({ default: m.AIInsights })));
const Settings = lazy(() => import('@/pages/Settings').then(m => ({ default: m.Settings })));

const PlaceholderPage = lazy(() => import('@/pages/PlaceholderPage').then(m => ({ default: m.PlaceholderPage })));

// A simple fallback for Suspense
function PageLoader() {
  return (
    <div className="flex-1 flex items-center justify-center min-h-[60vh]">
      <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public */}
        <Route path={ROUTES.ROOT} element={<Suspense fallback={<PageLoader />}><LandingPage /></Suspense>} />
        
        {/* Auth */}
        <Route path={ROUTES.LOGIN} element={
          <GuestRoute>
            <Suspense fallback={<PageLoader />}><Login /></Suspense>
          </GuestRoute>
        } />
        
        <Route path={ROUTES.FORGOT_PASSWORD} element={
          <GuestRoute>
            <Suspense fallback={<PageLoader />}><ForgotPasswordPage /></Suspense>
          </GuestRoute>
        } />

        {/* Protected App Shell */}
        <Route element={
          <ProtectedRoute>
            <AppLayout />
          </ProtectedRoute>
        }>
          <Route path={ROUTES.DASHBOARD} element={
            <Suspense fallback={<PageLoader />}><RoleDashboardRedirect /></Suspense>
          } />
          <Route path={ROUTES.DASHBOARD_ADMIN} element={
            <DashboardRoleGuard requiredRole="ADMIN">
              <Suspense fallback={<PageLoader />}><AdminDashboard /></Suspense>
            </DashboardRoleGuard>
          } />
          <Route path={ROUTES.DASHBOARD_MANAGER} element={
            <DashboardRoleGuard requiredRole="MANAGER">
              <Suspense fallback={<PageLoader />}><ManagerDashboard /></Suspense>
            </DashboardRoleGuard>
          } />
          <Route path={ROUTES.DASHBOARD_EMPLOYEE} element={
            <DashboardRoleGuard requiredRole="EMPLOYEE">
              <Suspense fallback={<PageLoader />}><EmployeeDashboard /></Suspense>
            </DashboardRoleGuard>
          } />
          <Route path={ROUTES.UNAUTHORIZED} element={
            <Suspense fallback={<PageLoader />}><UnauthorizedPage /></Suspense>
          } />
          <Route path={ROUTES.EMPLOYEES} element={
            <Suspense fallback={<PageLoader />}><EmployeesPage /></Suspense>
          } />
          <Route path={ROUTES.EMPLOYEE_PROFILE} element={
            <Suspense fallback={<PageLoader />}><EmployeeDetailsPage /></Suspense>
          } />
          <Route path={ROUTES.PIPELINE} element={
            <Suspense fallback={<PageLoader />}><PipelinePage /></Suspense>
          } />
          <Route path={ROUTES.PIPELINE_HISTORY} element={
            <Suspense fallback={<PageLoader />}><PipelineHistoryPage /></Suspense>
          } />
          <Route path={ROUTES.PIPELINE_MONITOR} element={
            <Suspense fallback={<PageLoader />}><PipelineRunPage /></Suspense>
          } />
          <Route path={ROUTES.REVIEWS} element={
            <Suspense fallback={<PageLoader />}><ReviewsPage /></Suspense>
          } />
          <Route path={ROUTES.REVIEW_DETAIL} element={
            <Suspense fallback={<PageLoader />}><ReviewDetailsPage /></Suspense>
          } />
          <Route path={ROUTES.INSIGHTS} element={
            <Suspense fallback={<PageLoader />}><AIInsights /></Suspense>
          } />
          <Route path={ROUTES.REPORTS} element={
            <Suspense fallback={<PageLoader />}><ReportsPage /></Suspense>
          } />
          <Route path={ROUTES.REPORT_DETAIL} element={
            <Suspense fallback={<PageLoader />}><ReportDetailsPage /></Suspense>
          } />
          <Route path={ROUTES.EXPLAINABILITY} element={
            <Suspense fallback={<PageLoader />}><ExplainabilityDetailsPage /></Suspense>
          } />
          <Route path={ROUTES.SETTINGS} element={
            <Suspense fallback={<PageLoader />}><Settings /></Suspense>
          } />

          {/* Placeholders */}
          <Route path={ROUTES.ORGANIZATIONS} element={<Suspense fallback={<PageLoader />}><PlaceholderPage /></Suspense>} />
          <Route path={ROUTES.POLICIES} element={<Suspense fallback={<PageLoader />}><PlaceholderPage /></Suspense>} />
          <Route path={ROUTES.AUDIT_LOGS} element={<Suspense fallback={<PageLoader />}><PlaceholderPage /></Suspense>} />
          <Route path={ROUTES.SECURITY} element={<Suspense fallback={<PageLoader />}><PlaceholderPage /></Suspense>} />
          <Route path={ROUTES.PERFORMANCE} element={<Suspense fallback={<PageLoader />}><PlaceholderPage /></Suspense>} />
          <Route path={ROUTES.GOALS} element={<Suspense fallback={<PageLoader />}><PlaceholderPage /></Suspense>} />
          <Route path={ROUTES.FEEDBACK} element={<Suspense fallback={<PageLoader />}><PlaceholderPage /></Suspense>} />
          <Route path={ROUTES.CAREER} element={<Suspense fallback={<PageLoader />}><PlaceholderPage /></Suspense>} />
          <Route path={ROUTES.ACHIEVEMENTS} element={<Suspense fallback={<PageLoader />}><PlaceholderPage /></Suspense>} />
          <Route path={ROUTES.LEARNING} element={<Suspense fallback={<PageLoader />}><PlaceholderPage /></Suspense>} />
          <Route path={ROUTES.APPROVALS} element={<Suspense fallback={<PageLoader />}><PlaceholderPage /></Suspense>} />
        </Route>

        {/* Fallback 404 */}
        <Route path="*" element={<Suspense fallback={<PageLoader />}><NotFoundPage /></Suspense>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;