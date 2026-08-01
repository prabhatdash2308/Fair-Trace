import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { BarChart3, Activity, ShieldCheck, Clock, Plus, ArrowRight, Zap } from 'lucide-react'
import { cyclesApi, type ReviewCycle } from '../api'
import { useAuthStore } from '../store'
import { statusBadge, formatDate } from '../utils'

export default function DashboardPage() {
  const { user } = useAuthStore()
  const navigate = useNavigate()
  const [cycles, setCycles] = useState<{ items: ReviewCycle[]; total: number }>({ items: [], total: 0 })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    cyclesApi.list(0, 5)
      .then(data => setCycles(data))
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  const statusCounts = cycles.items.reduce((acc, c) => {
    acc[c.status] = (acc[c.status] || 0) + 1
    return acc
  }, {} as Record<string, number>)

  return (
    <div className="fade-in">
      {/* Header */}
      <div className="page-header">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="page-title">Dashboard</h1>
            <p className="page-subtitle">
              Welcome back, <strong>{user?.full_name}</strong> — {user?.role}
            </p>
          </div>
          {(user?.role === 'MANAGER' || user?.role === 'ADMIN') && (
            <button className="btn btn-primary" onClick={() => navigate('/cycles/new')}>
              <Plus size={15} /> New Review Cycle
            </button>
          )}
        </div>
      </div>

      {/* Stats */}
      <div className="grid-4 mb-6">
        <div className="stat-card">
          <div className="stat-label">Total Cycles</div>
          <div className="stat-value">{cycles.total}</div>
          <div className="stat-sub">All time</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Active</div>
          <div className="stat-value" style={{ fontSize: 28 }}>{statusCounts['ACTIVE'] || 0}</div>
          <div className="stat-sub">Awaiting pipeline</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Pending Approval</div>
          <div className="stat-value" style={{ fontSize: 28 }}>{statusCounts['PENDING_APPROVAL'] || 0}</div>
          <div className="stat-sub">Requires review</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Completed</div>
          <div className="stat-value" style={{ fontSize: 28 }}>{statusCounts['COMPLETED'] || 0}</div>
          <div className="stat-sub">Finalized</div>
        </div>
      </div>

      {/* Recent Cycles */}
      <div className="card mb-6">
        <div className="card-header">
          <span className="card-title">Recent Review Cycles</span>
          <button className="btn btn-sm btn-secondary" onClick={() => navigate('/cycles')}>
            View all <ArrowRight size={13} />
          </button>
        </div>
        <div>
          {loading ? (
            <div style={{ padding: 40, textAlign: 'center' }}>
              <div className="spinner-lg" style={{ margin: '0 auto' }} />
            </div>
          ) : cycles.items.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">📋</div>
              <div className="empty-title">No review cycles yet</div>
              <div className="empty-desc">
                {user?.role === 'EMPLOYEE'
                  ? 'Your manager has not started a review cycle for you yet.'
                  : 'Create your first review cycle to get started.'}
              </div>
              {user?.role !== 'EMPLOYEE' && (
                <button className="btn btn-primary mt-4" onClick={() => navigate('/cycles/new')}>
                  <Plus size={15} /> Create Review Cycle
                </button>
              )}
            </div>
          ) : (
            <div className="table-container" style={{ border: 'none', borderRadius: 0 }}>
              <table>
                <thead>
                  <tr>
                    <th>Title</th>
                    <th>Status</th>
                    <th>Period</th>
                    <th>Created</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  {cycles.items.map(c => (
                    <tr key={c.id} style={{ cursor: 'pointer' }} onClick={() => navigate(`/cycles/${c.id}`)}>
                      <td style={{ fontWeight: 500 }}>{c.title}</td>
                      <td>{statusBadge(c.status)}</td>
                      <td style={{ color: 'var(--text-secondary)', fontSize: 13 }}>
                        {formatDate(c.review_period_start)} – {formatDate(c.review_period_end)}
                      </td>
                      <td style={{ color: 'var(--text-muted)', fontSize: 13 }}>{formatDate(c.created_at)}</td>
                      <td>
                        <ArrowRight size={14} color="var(--text-muted)" />
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

      {/* Architecture callout */}
      <div className="card" style={{ background: 'var(--gradient-surface)', borderColor: 'var(--border-glass)' }}>
        <div className="card-body">
          <div className="flex items-center gap-3 mb-3">
            <Zap size={18} color="var(--accent-primary)" />
            <span style={{ fontWeight: 600, fontSize: 14 }}>ReviewGuard AI Pipeline</span>
            <span className="badge badge-purple">9 Agents</span>
          </div>
          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
            {['Intake', 'Embedding', 'Evidence Retrieval', 'Bias Detection', 'Performance Analysis',
              'Report Generation', 'Explainability', 'Human Approval', 'Finalization'].map((step, i) => (
              <div key={step} style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                <span style={{
                  padding: '3px 10px',
                  background: 'rgba(124,58,237,0.12)',
                  border: '1px solid var(--border-glass)',
                  borderRadius: 20,
                  fontSize: 11.5,
                  fontWeight: 500,
                  color: 'var(--text-accent)',
                }}>{step}</span>
                {i < 8 && <span style={{ color: 'var(--text-muted)', fontSize: 10 }}>→</span>}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
