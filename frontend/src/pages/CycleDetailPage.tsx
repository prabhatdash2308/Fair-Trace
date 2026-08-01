import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Plus, Play, FileText, Upload, Zap, ChevronRight } from 'lucide-react'
import { cyclesApi, reportsApi, type ReviewCycle, type ReviewInput, type Report } from '../api'
import { useAuthStore } from '../store'
import { statusBadge, formatDate } from '../utils'

function SubmitInputModal({ cycleId, onClose, onDone }: { cycleId: string; onClose: () => void; onDone: () => void }) {
  const [inputType, setInputType] = useState('SELF_ASSESSMENT')
  const [contentText, setContentText] = useState('')
  const [isAnonymized, setIsAnonymized] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async () => {
    if (contentText.trim().length < 50) { setError('Content must be at least 50 characters.'); return }
    setLoading(true)
    try {
      await cyclesApi.submitInput(cycleId, { input_type: inputType, content_text: contentText, is_anonymized: isAnonymized })
      onDone()
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to submit input')
    } finally { setLoading(false) }
  }

  return (
    <div style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.7)', backdropFilter: 'blur(8px)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
      <div className="card" style={{ width: 540, maxWidth: '90vw', borderColor: 'var(--border-glass)' }}>
        <div className="card-header">
          <span className="card-title">Submit Review Input</span>
          <button onClick={onClose} style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-muted)', fontSize: 18 }}>✕</button>
        </div>
        <div className="card-body">
          {error && <div className="alert alert-error">{error}</div>}
          <div className="form-group">
            <label className="form-label">Input Type</label>
            <select className="form-input" value={inputType} onChange={e => setInputType(e.target.value)}>
              {['SELF_ASSESSMENT', 'MANAGER_NOTE', 'PEER_REVIEW', 'PROJECT_OUTCOME', 'GOAL', 'MEETING_NOTE'].map(t => (
                <option key={t} value={t}>{t.replace(/_/g, ' ')}</option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label className="form-label">Content (min 50 characters)</label>
            <textarea className="form-input" placeholder="Describe performance observations, outcomes, or goals..." value={contentText} onChange={e => setContentText(e.target.value)} rows={6} />
            <p style={{ fontSize: 11.5, color: 'var(--text-muted)', marginTop: 4 }}>{contentText.length} characters</p>
          </div>
          <div className="form-group" style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <input type="checkbox" id="anon" checked={isAnonymized} onChange={e => setIsAnonymized(e.target.checked)} style={{ accentColor: 'var(--accent-primary)' }} />
            <label htmlFor="anon" style={{ fontSize: 13, color: 'var(--text-secondary)' }}>Anonymize this input (hides submitter identity)</label>
          </div>
          <div className="flex" style={{ gap: 12, justifyContent: 'flex-end' }}>
            <button className="btn btn-secondary" onClick={onClose}>Cancel</button>
            <button className="btn btn-primary" onClick={handleSubmit} disabled={loading}>
              {loading ? <><span className="spinner" /> Submitting...</> : <><Upload size={14} /> Submit Input</>}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default function CycleDetailPage() {
  const { cycleId } = useParams()
  const navigate = useNavigate()
  const { user } = useAuthStore()
  const [cycle, setCycle] = useState<ReviewCycle | null>(null)
  const [inputs, setInputs] = useState<ReviewInput[]>([])
  const [reports, setReports] = useState<Report[]>([])
  const [loading, setLoading] = useState(true)
  const [showInputModal, setShowInputModal] = useState(false)

  const fetchAll = async () => {
    if (!cycleId) return
    try {
      const [c, i] = await Promise.all([
        cyclesApi.get(cycleId),
        cyclesApi.getInputs(cycleId).catch(() => [])
      ])
      setCycle(c)
      setInputs(i)
    } finally { setLoading(false) }
  }

  useEffect(() => { fetchAll() }, [cycleId])

  const canSubmitInput = cycle?.status === 'ACTIVE'
  const canTrigger = cycle?.status === 'ACTIVE' && inputs.length > 0 && (user?.role === 'MANAGER' || user?.role === 'ADMIN')

  if (loading) return <div style={{ textAlign: 'center', padding: 80 }}><div className="spinner-lg" style={{ margin: '0 auto' }} /></div>
  if (!cycle) return <div className="empty-state"><div className="empty-title">Cycle not found</div></div>

  return (
    <div className="fade-in">
      {showInputModal && (
        <SubmitInputModal
          cycleId={cycle.id}
          onClose={() => setShowInputModal(false)}
          onDone={() => { setShowInputModal(false); fetchAll() }}
        />
      )}

      <div className="page-header">
        <button onClick={() => navigate('/cycles')} style={{ fontSize: 12.5, color: 'var(--text-muted)', background: 'none', border: 'none', cursor: 'pointer', marginBottom: 12 }}>← Back to Cycles</button>
        <div className="flex items-center justify-between">
          <div>
            <h1 className="page-title">{cycle.title}</h1>
            <div className="flex items-center gap-3 mt-2">
              {statusBadge(cycle.status)}
              <span style={{ fontSize: 13, color: 'var(--text-muted)' }}>
                {formatDate(cycle.review_period_start)} — {formatDate(cycle.review_period_end)}
              </span>
            </div>
          </div>
          <div className="flex items-center gap-3">
            {canSubmitInput && (
              <button className="btn btn-secondary" onClick={() => setShowInputModal(true)}>
                <Plus size={14} /> Add Input
              </button>
            )}
            {canTrigger && (
              <button className="btn btn-primary" onClick={() => navigate(`/cycles/${cycleId}/pipeline`)}>
                <Zap size={14} /> Run Pipeline
              </button>
            )}
          </div>
        </div>
      </div>

      <div className="grid-2" style={{ gap: 24 }}>
        {/* Inputs */}
        <div>
          <div className="card">
            <div className="card-header">
              <span className="card-title">Review Inputs</span>
              <span className="badge badge-purple">{inputs.length}</span>
            </div>
            <div style={{ padding: '12px 16px' }}>
              {inputs.length === 0 ? (
                <div className="empty-state" style={{ padding: '30px 20px' }}>
                  <div className="empty-icon" style={{ fontSize: 32 }}>📝</div>
                  <div className="empty-title" style={{ fontSize: 15 }}>No inputs yet</div>
                  <div className="empty-desc">Submit review inputs to enable pipeline analysis.</div>
                </div>
              ) : inputs.map(inp => (
                <div key={inp.id} style={{ padding: '12px 0', borderBottom: '1px solid var(--border-subtle)' }}>
                  <div className="flex items-center justify-between mb-1">
                    <span className="badge badge-blue" style={{ fontSize: 10 }}>{inp.input_type.replace(/_/g, ' ')}</span>
                    {inp.is_anonymized && <span className="badge badge-gray" style={{ fontSize: 10 }}>Anonymized</span>}
                  </div>
                  <p style={{ fontSize: 13, color: 'var(--text-secondary)', lineHeight: 1.5, marginTop: 6 }}>
                    {inp.content_text.substring(0, 180)}{inp.content_text.length > 180 ? '...' : ''}
                  </p>
                  <p style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 6 }}>{formatDate(inp.submitted_at)}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Cycle info + status actions */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <div className="card">
            <div className="card-header"><span className="card-title">Cycle Information</span></div>
            <div className="card-body">
              {[
                { label: 'Status', value: statusBadge(cycle.status) },
                { label: 'Employee ID', value: <span className="mono" style={{ fontSize: 11 }}>{cycle.employee_id}</span> },
                { label: 'Manager ID', value: <span className="mono" style={{ fontSize: 11 }}>{cycle.manager_id}</span> },
                { label: 'Period Start', value: formatDate(cycle.review_period_start) },
                { label: 'Period End', value: formatDate(cycle.review_period_end) },
                { label: 'Created', value: formatDate(cycle.created_at) },
                { label: 'Inputs', value: `${inputs.length} submitted` },
              ].map(({ label, value }) => (
                <div key={label} style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', borderBottom: '1px solid var(--border-subtle)', fontSize: 13 }}>
                  <span style={{ color: 'var(--text-muted)' }}>{label}</span>
                  <span style={{ fontWeight: 500 }}>{value}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Status flow guidance */}
          <div className="card" style={{ background: 'var(--gradient-surface)', borderColor: 'var(--border-glass)' }}>
            <div className="card-body">
              <p style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-muted)', marginBottom: 12, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Review Cycle Workflow</p>
              {['DRAFT', 'ACTIVE', 'PROCESSING', 'PENDING_APPROVAL', 'COMPLETED'].map((s, i) => (
                <div key={s} style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
                  <div style={{
                    width: 8, height: 8, borderRadius: '50%',
                    background: cycle.status === s ? 'var(--accent-primary)' : i < ['DRAFT','ACTIVE','PROCESSING','PENDING_APPROVAL','COMPLETED'].indexOf(cycle.status) ? '#10b981' : 'var(--border-subtle)',
                    flexShrink: 0,
                  }} />
                  <span style={{
                    fontSize: 12.5,
                    color: cycle.status === s ? 'var(--text-accent)' : 'var(--text-muted)',
                    fontWeight: cycle.status === s ? 600 : 400,
                  }}>{s.replace(/_/g, ' ')}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
