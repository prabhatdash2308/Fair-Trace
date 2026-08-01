import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AppLayout } from '@/components/layout/AppLayout';
import { ProtectedRoute } from '@/guards/ProtectedRoute';
import { GuestRoute } from '@/guards/GuestRoute';
import { ROUTES } from '@/constants/routes';

// ── Pages (existing — preserved as-is) ───────────────────────────────
import { LandingPage }        from '@/pages/LandingPage';
import { Dashboard }          from '@/pages/Dashboard';
import EmployeesPage          from '@/pages/EmployeesPage';
import EmployeeDetailsPage    from '@/pages/EmployeeDetailsPage';
import PipelinePage           from '@/pages/PipelinePage';
import PipelineHistoryPage    from '@/pages/PipelineHistoryPage';
import PipelineRunPage        from '@/pages/PipelineRunPage';
import { AIInsights }         from '@/pages/AIInsights';
import { ReviewCycles }       from '@/pages/ReviewCycles';
import { Reports }            from '@/pages/Reports';
import { Settings }           from '@/pages/Settings';
import { Login }              from '@/pages/Login';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public */}
        <Route path={ROUTES.ROOT}  element={<LandingPage />} />
        <Route
          path={ROUTES.LOGIN}
          element={
            <GuestRoute>
              <Login />
            </GuestRoute>
          }
        />

        {/* Protected app shell */}
        <Route
          element={
            <ProtectedRoute>
              <AppLayout />
            </ProtectedRoute>
          }
        >
          <Route path={ROUTES.DASHBOARD}        element={<Dashboard />} />
          <Route path={ROUTES.EMPLOYEES}        element={<EmployeesPage />} />
          <Route path={ROUTES.EMPLOYEE_PROFILE} element={<EmployeeDetailsPage />} />
          <Route path={ROUTES.PIPELINE}         element={<PipelinePage />} />
          <Route path={ROUTES.PIPELINE_HISTORY} element={<PipelineHistoryPage />} />
          <Route path={ROUTES.PIPELINE_MONITOR} element={<PipelineRunPage />} />
          <Route path={ROUTES.REVIEWS}          element={<ReviewCycles />} />
          <Route path={ROUTES.INSIGHTS}         element={<AIInsights />} />
          <Route path={ROUTES.REPORTS}          element={<Reports />} />
          <Route path={ROUTES.SETTINGS}         element={<Settings />} />
        </Route>

        {/* Fallback */}
        <Route path="*" element={<Navigate to={ROUTES.ROOT} replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;