import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Plus, ChevronRight, Filter } from 'lucide-react'
import { cyclesApi, type ReviewCycle } from '../api'
import { useAuthStore } from '../store'
import { statusBadge, formatDate } from '../utils'
import { EmptyState } from '@/components/shared/EmptyState'
import { FileText } from 'lucide-react'

export default function CyclesListPage() {
  const navigate = useNavigate()
  const { user } = useAuthStore()
  const [data, setData] = useState<{ items: ReviewCycle[]; total: number }>({ items: [], total: 0 })
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('')

  useEffect(() => {
    cyclesApi.list(0, 50)
      .then(d => setData(d))
      .finally(() => setLoading(false))
  }, [])

  const filtered = data.items.filter(c =>
    c.title.toLowerCase().includes(filter.toLowerCase()) ||
    c.status.toLowerCase().includes(filter.toLowerCase())
  )

  return (
    <div className="fade-in">
      <div className="page-header">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="page-title">Review Cycles</h1>
            <p className="page-subtitle">{data.total} total cycles</p>
          </div>
          {(user?.role === 'MANAGER' || user?.role === 'ADMIN') && (
            <button className="btn btn-primary" onClick={() => navigate('/cycles/new')}>
              <Plus size={15} /> New Cycle
            </button>
          )}
        </div>
      </div>

      {/* Search */}
      <div style={{ display: 'flex', gap: 12, marginBottom: 20 }}>
        <input
          className="form-input"
          placeholder="Filter by title or status..."
          value={filter}
          onChange={e => setFilter(e.target.value)}
          style={{ maxWidth: 360 }}
        />
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: 80 }}>
          <div className="spinner-lg" style={{ margin: '0 auto' }} />
        </div>
      ) : filtered.length === 0 ? (
        <EmptyState
          icon={FileText}
          title="No review cycles found"
          description="You haven't created any review cycles yet."
          action={
            user?.role !== 'EMPLOYEE'
              ? {
                  label: "Create First Cycle",
                  onClick: () => navigate('/cycles/new')
                }
              : undefined
          }
        />
      ) : (
        <div className="card">
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
                {filtered.map(c => (
                  <tr key={c.id} style={{ cursor: 'pointer' }} onClick={() => navigate(`/cycles/${c.id}`)}>
                    <td style={{ fontWeight: 500 }}>{c.title}</td>
                    <td>{statusBadge(c.status)}</td>
                    <td style={{ fontSize: 13, color: 'var(--text-secondary)' }}>
                      {formatDate(c.review_period_start)} – {formatDate(c.review_period_end)}
                    </td>
                    <td style={{ fontSize: 13, color: 'var(--text-muted)' }}>{formatDate(c.created_at)}</td>
                    <td><ChevronRight size={15} color="var(--text-muted)" /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}
