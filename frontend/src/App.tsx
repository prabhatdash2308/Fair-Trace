import React, { useEffect } from 'react'
import { Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom'
import { LayoutDashboard, Target, Users, Settings, LogOut, FileText } from 'lucide-react'
import { useAuthStore } from './store'
import api from './api'

// Pages
import LoginPage from './pages/LoginPage'
import DashboardPage from './pages/DashboardPage'
import CyclesListPage from './pages/CyclesListPage'
import CreateCyclePage from './pages/CreateCyclePage'
import CycleDetailPage from './pages/CycleDetailPage'
import PipelineMonitorPage from './pages/PipelineMonitorPage'
import ReportDetailPage from './pages/ReportDetailPage'

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuthStore()
  if (!isAuthenticated) return <Navigate to="/login" replace />
  return <>{children}</>
}

function Sidebar() {
  const { user, logout } = useAuthStore()
  const navigate = useNavigate()
  const location = useLocation()

  const navItems = [
    { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { name: 'Review Cycles', path: '/cycles', icon: Target },
    { name: 'Reports', path: '/reports', icon: FileText, disabled: true },
    { name: 'Team', path: '/team', icon: Users, disabled: true },
  ]

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="sidebar">
      <div className="sidebar-logo">
        <div className="logo-icon">🛡️</div>
        <div className="logo-text">
          <h1>ReviewGuard AI</h1>
          <span>Performance Intelligence</span>
        </div>
      </div>

      <nav className="sidebar-nav">
        <div className="nav-section-label">Main Menu</div>
        {navItems.map((item) => {
          const Icon = item.icon
          const isActive = location.pathname.startsWith(item.path)
          return (
            <button
              key={item.name}
              className={`nav-item ${isActive ? 'active' : ''}`}
              onClick={() => !item.disabled && navigate(item.path)}
              style={{ opacity: item.disabled ? 0.5 : 1, cursor: item.disabled ? 'not-allowed' : 'pointer' }}
              title={item.disabled ? 'Coming soon' : ''}
            >
              <Icon size={16} />
              <span>{item.name}</span>
            </button>
          )
        })}
      </nav>

      <div className="sidebar-user">
        <div className="user-avatar">{user?.full_name?.charAt(0) || 'U'}</div>
        <div className="user-info">
          <div className="user-name">{user?.full_name}</div>
          <div className="user-role">{user?.role}</div>
        </div>
        <button onClick={handleLogout} className="btn-icon" style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }} title="Log out">
          <LogOut size={16} />
        </button>
      </div>
    </div>
  )
}

function AppLayout() {
  return (
    <div className="app-layout">
      <Sidebar />
      <main className="main-content">
        <div style={{ maxWidth: 1100, margin: '0 auto' }}>
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/cycles" element={<CyclesListPage />} />
            <Route path="/cycles/new" element={<CreateCyclePage />} />
            <Route path="/cycles/:cycleId" element={<CycleDetailPage />} />
            <Route path="/cycles/:cycleId/pipeline" element={<PipelineMonitorPage />} />
            <Route path="/reports/:reportId" element={<ReportDetailPage />} />
          </Routes>
        </div>
      </main>
    </div>
  )
}

export default function App() {
  // Validate token on mount
  useEffect(() => {
    const token = localStorage.getItem('rg_token')
    if (token) {
      // Just a light touch to ensure token is valid; if 401, interceptor will logout
      api.get('/users?limit=1').catch(() => {})
    }
  }, [])

  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/*"
        element={
          <ProtectedRoute>
            <AppLayout />
          </ProtectedRoute>
        }
      />
    </Routes>
  )
}
