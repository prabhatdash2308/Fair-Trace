import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Shield, Eye, EyeOff, Loader } from 'lucide-react'
import { authApi } from '../api'
import { useAuthStore } from '../store'

export default function LoginPage() {
  const navigate = useNavigate()
  const { login } = useAuthStore()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPwd, setShowPwd] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const res = await authApi.login(email, password)
      login(res.access_token, res.user)
      navigate('/dashboard')
    } catch (err: any) {
      setError(err.response?.data?.message || 'Login failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-container">
      <div className="login-card fade-in">
        {/* Logo */}
        <div className="flex items-center gap-3 mb-6">
          <div className="logo-icon" style={{ width: 44, height: 44, fontSize: 22 }}>🛡️</div>
          <div>
            <h1 style={{ fontSize: 20, fontWeight: 800, background: 'var(--gradient-brand)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
              ReviewGuard AI
            </h1>
            <p style={{ fontSize: 11, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
              Evidence-Grounded Performance Intelligence
            </p>
          </div>
        </div>

        <h2 style={{ fontSize: 22, fontWeight: 700, marginBottom: 6 }}>Welcome back</h2>
        <p style={{ fontSize: 13.5, color: 'var(--text-secondary)', marginBottom: 28 }}>
          Sign in to access your performance review dashboard.
        </p>

        {error && <div className="alert alert-error" style={{ marginBottom: 20 }}>{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label" htmlFor="email">Email address</label>
            <input
              id="email"
              type="email"
              className="form-input"
              value={email}
              onChange={e => setEmail(e.target.value)}
              placeholder="you@company.com"
              required
              autoComplete="email"
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="password">Password</label>
            <div style={{ position: 'relative' }}>
              <input
                id="password"
                type={showPwd ? 'text' : 'password'}
                className="form-input"
                value={password}
                onChange={e => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                style={{ paddingRight: 44 }}
              />
              <button
                type="button"
                onClick={() => setShowPwd(!showPwd)}
                style={{
                  position: 'absolute', right: 12, top: '50%', transform: 'translateY(-50%)',
                  background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-muted)',
                  display: 'flex', alignItems: 'center',
                }}
              >
                {showPwd ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            </div>
          </div>

          <button type="submit" className="btn btn-primary" style={{ width: '100%', justifyContent: 'center', padding: '12px' }} disabled={loading}>
            {loading ? <><span className="spinner" /> Signing in...</> : 'Sign in'}
          </button>
        </form>

        {/* Demo credentials hint */}
        <div style={{ marginTop: 24, padding: '14px 16px', background: 'rgba(124,58,237,0.05)', border: '1px solid var(--border-glass)', borderRadius: 'var(--radius-md)' }}>
          <p style={{ fontSize: 11, fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: 8 }}>Demo credentials</p>
          {[
            { role: 'Admin', email: 'admin@reviewguard.ai', pwd: 'admin123456' },
            { role: 'Manager', email: 'manager@reviewguard.ai', pwd: 'manager123456' },
            { role: 'Employee', email: 'employee@reviewguard.ai', pwd: 'employee123456' },
          ].map(c => (
            <div key={c.role} style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, marginBottom: 4 }}>
              <span style={{ color: 'var(--text-accent)', fontWeight: 500 }}>{c.role}</span>
              <button
                className="btn btn-sm btn-secondary"
                style={{ padding: '2px 10px', fontSize: 11 }}
                onClick={() => { setEmail(c.email); setPassword(c.pwd) }}
                type="button"
              >Fill</button>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
