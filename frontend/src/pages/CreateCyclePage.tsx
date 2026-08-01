import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { usersApi, cyclesApi } from '../api'

export default function CreateCyclePage() {
  const navigate = useNavigate()
  const [form, setForm] = useState({
    employee_id: '',
    title: '',
    review_period_start: '',
    review_period_end: '',
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const cycle = await cyclesApi.create(form)
      navigate(`/cycles/${cycle.id}`)
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to create review cycle')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fade-in" style={{ maxWidth: 560 }}>
      <div className="page-header">
        <button onClick={() => navigate('/cycles')} style={{ fontSize: 12.5, color: 'var(--text-muted)', background: 'none', border: 'none', cursor: 'pointer', marginBottom: 12 }}>
          ← Back to Cycles
        </button>
        <h1 className="page-title">Create Review Cycle</h1>
        <p className="page-subtitle">Start a new performance review cycle for an employee.</p>
      </div>

      <div className="card">
        <div className="card-body">
          {error && <div className="alert alert-error">{error}</div>}

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label className="form-label">Review Title</label>
              <input
                className="form-input"
                placeholder="e.g. Q3 2026 Performance Review"
                value={form.title}
                onChange={e => setForm({ ...form, title: e.target.value })}
                required
                minLength={2}
              />
            </div>

            <div className="form-group">
              <label className="form-label">Employee ID</label>
              <input
                className="form-input"
                placeholder="UUID of the employee"
                value={form.employee_id}
                onChange={e => setForm({ ...form, employee_id: e.target.value })}
                required
              />
              <p style={{ fontSize: 11.5, color: 'var(--text-muted)', marginTop: 4 }}>
                You can find Employee IDs in the Users section.
              </p>
            </div>

            <div className="grid-2">
              <div className="form-group">
                <label className="form-label">Period Start</label>
                <input
                  type="date"
                  className="form-input"
                  value={form.review_period_start}
                  onChange={e => setForm({ ...form, review_period_start: e.target.value })}
                  required
                />
              </div>
              <div className="form-group">
                <label className="form-label">Period End</label>
                <input
                  type="date"
                  className="form-input"
                  value={form.review_period_end}
                  onChange={e => setForm({ ...form, review_period_end: e.target.value })}
                  required
                />
              </div>
            </div>

            <div style={{ display: 'flex', gap: 12, marginTop: 8 }}>
              <button type="button" className="btn btn-secondary" onClick={() => navigate('/cycles')}>Cancel</button>
              <button type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? <><span className="spinner" /> Creating...</> : 'Create Review Cycle'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}
