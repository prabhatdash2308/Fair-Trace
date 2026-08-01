import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ShieldAlert, CheckCircle2, AlertTriangle, BarChart3, FileText, ThumbsUp, RefreshCw, MessageSquare, XCircle } from 'lucide-react'
import { reportsApi, cyclesApi, type Report, type Claim } from '../api'
import { useAuthStore } from '../store'
import { confidenceBadge, biasSeverityColor } from '../utils'
import { v4 as uuidv4 } from 'uuid'

function EvidencePanel({ claim }: { claim: Claim }) {
  const [open, setOpen] = useState(false)
  return (
    <div className="evidence-citation">
      <div className="flex items-center justify-between" style={{ cursor: 'pointer' }} onClick={() => setOpen(!open)}>
        <div className="flex items-center gap-2">
          <span className={`badge ${confidenceBadge(claim.confidence)}`}>{claim.confidence}</span>
          <span style={{ fontSize: 13.5, fontWeight: 500 }}>{claim.dimension}</span>
        </div>
        <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>{claim.citations.length} citations {open ? '▲' : '▼'}</span>
      </div>
      <p style={{ fontSize: 14, marginTop: 8, lineHeight: 1.6 }}>{claim.claim_text}</p>
      {claim.explanation && (
        <p style={{ fontSize: 12.5, color: 'var(--text-secondary)', marginTop: 6, lineHeight: 1.5 }}>
          <em>{claim.explanation}</em>
        </p>
      )}
      {open && claim.citations.map((cit, i) => (
        <div key={cit.id} style={{ marginTop: 10 }}>
          <div className="flex items-center justify-between mb-2">
            <span style={{ fontSize: 11, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Citation #{cit.retrieval_rank}
            </span>
            <span style={{ fontSize: 11, color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
              {(cit.similarity_score * 100).toFixed(0)}% match
            </span>
          </div>
          <p className="citation-passage">"{cit.extracted_passage}"</p>
          <div className="similarity-bar">
            <div className="similarity-fill" style={{ width: `${cit.similarity_score * 100}%` }} />
          </div>
        </div>
      ))}
    </div>
  )
}

function ApprovalModal({ reportId, onClose, onDone }: {
  reportId: string
  onClose: () => void
  onDone: () => void
}) {
  const [action, setAction] = useState<'APPROVE' | 'REVISION_REQUESTED' | 'REJECT'>('APPROVE')
  const [reason, setReason] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async () => {
    if (reason.trim().length < 10) { setError('Reason must be at least 10 characters.'); return }
    setLoading(true)
    try {
      await reportsApi.approve(reportId, { action, reason, idempotency_key: uuidv4() })
      onDone()
    } catch (err: any) {
      setError(err.response?.data?.message || 'Action failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{
      position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.7)', backdropFilter: 'blur(8px)',
      display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000,
    }}>
      <div className="card" style={{ width: 480, maxWidth: '90vw', borderColor: 'var(--border-glass)' }}>
        <div className="card-header">
          <span className="card-title">Review Action</span>
          <button onClick={onClose} style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-muted)' }}>
            <XCircle size={18} />
          </button>
        </div>
        <div className="card-body">
          {error && <div className="alert alert-error">{error}</div>}

          <div className="form-group">
            <label className="form-label">Action</label>
            <div style={{ display: 'flex', gap: 8 }}>
              {(['APPROVE', 'REVISION_REQUESTED', 'REJECT'] as const).map(a => (
                <button
                  key={a}
                  className={`btn btn-sm ${action === a ? 'btn-primary' : 'btn-secondary'}`}
                  onClick={() => setAction(a)}
                >
                  {a === 'APPROVE' ? '✓ Approve' : a === 'REVISION_REQUESTED' ? '↻ Revise' : '✗ Reject'}
                </button>
              ))}
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">Justification (required)</label>
            <textarea
              className="form-input"
              placeholder="Explain your decision in detail (min 10 characters)..."
              value={reason}
              onChange={e => setReason(e.target.value)}
              rows={4}
            />
          </div>

          <div style={{ display: 'flex', gap: 12, justifyContent: 'flex-end' }}>
            <button className="btn btn-secondary" onClick={onClose}>Cancel</button>
            <button className="btn btn-primary" onClick={handleSubmit} disabled={loading}>
              {loading ? <><span className="spinner" /> Processing...</> : 'Submit'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default function ReportDetailPage() {
  const { reportId } = useParams()
  const navigate = useNavigate()
  const { user } = useAuthStore()
  const [report, setReport] = useState<Report | null>(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<'claims' | 'bias' | 'summary'>('summary')
  const [showApproval, setShowApproval] = useState(false)

  const fetchReport = async () => {
    if (!reportId) return
    try {
      const data = await reportsApi.get(reportId)
      setReport(data)
    } catch (e) { console.error(e) }
    finally { setLoading(false) }
  }

  useEffect(() => { fetchReport() }, [reportId])

  if (loading) return <div style={{ textAlign: 'center', padding: 80 }}><div className="spinner-lg" style={{ margin: '0 auto' }} /></div>
  if (!report) return <div className="empty-state"><div className="empty-title">Report not found</div></div>

  const canApprove = (user?.role === 'MANAGER' || user?.role === 'ADMIN') && report.status === 'PENDING_APPROVAL'

  return (
    <div className="fade-in">
      {showApproval && (
        <ApprovalModal
          reportId={report.id}
          onClose={() => setShowApproval(false)}
          onDone={() => { setShowApproval(false); fetchReport() }}
        />
      )}

      {/* Header */}
      <div className="page-header">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="page-title">Performance Report</h1>
            <p className="page-subtitle">
              Version {report.version} · {report.status} ·
              Confidence: <strong style={{ color: report.confidence_score === 'HIGH' ? '#6ee7b7' : report.confidence_score === 'INSUFFICIENT' ? '#fca5a5' : '#fcd34d' }}>
                {report.confidence_score || 'Unknown'}
              </strong>
            </p>
          </div>
          <div className="flex items-center gap-3">
            {canApprove && (
              <button className="btn btn-primary" onClick={() => setShowApproval(true)}>
                <ThumbsUp size={14} /> Review Action
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Confidence explanation */}
      {report.confidence_explanation && (
        <div className="alert alert-info mb-4">
          <BarChart3 size={16} />
          <span>{report.confidence_explanation}</span>
        </div>
      )}

      {/* Bias warning */}
      {report.bias_flags.filter(f => f.severity === 'HIGH').length > 0 && (
        <div className="alert alert-warning mb-4">
          <AlertTriangle size={16} />
          <span>
            <strong>{report.bias_flags.filter(f => f.severity === 'HIGH').length} HIGH severity</strong> bias flags detected.
            Review the Bias Analysis tab before approving.
          </span>
        </div>
      )}

      {/* Tabs */}
      <div style={{ display: 'flex', gap: 4, marginBottom: 24, borderBottom: '1px solid var(--border-subtle)', paddingBottom: 0 }}>
        {(['summary', 'claims', 'bias'] as const).map(tab => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            style={{
              padding: '10px 20px',
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              fontSize: 13.5,
              fontWeight: 600,
              color: activeTab === tab ? 'var(--text-accent)' : 'var(--text-muted)',
              borderBottom: activeTab === tab ? '2px solid var(--accent-primary)' : '2px solid transparent',
              marginBottom: -1,
              fontFamily: 'var(--font-sans)',
              transition: 'all 0.15s',
            }}
          >
            {tab === 'summary' ? '📋 Executive Summary' : tab === 'claims' ? '🔍 Evidence & Claims' : '⚠️ Bias Analysis'}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      {activeTab === 'summary' && (
        <div className="grid-2 fade-in" style={{ gap: 24 }}>
          <div>
            <div className="card mb-4">
              <div className="card-header"><span className="card-title">Executive Summary</span></div>
              <div className="card-body">
                <p style={{ fontSize: 14.5, lineHeight: 1.8, color: 'var(--text-secondary)' }}>
                  {report.executive_summary || 'Summary not yet available.'}
                </p>
              </div>
            </div>
            {report.recommended_actions && report.recommended_actions.length > 0 && (
              <div className="card">
                <div className="card-header"><span className="card-title">Recommended Actions</span></div>
                <div className="card-body">
                  {report.recommended_actions.map((action, i) => (
                    <div key={i} style={{ display: 'flex', gap: 12, marginBottom: 14, padding: '12px 14px', background: 'rgba(124,58,237,0.05)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-glass)' }}>
                      <span style={{ fontSize: 18, lineHeight: 1 }}>→</span>
                      <p style={{ fontSize: 13.5, lineHeight: 1.6 }}>{action}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
          {/* Approval info */}
          <div>
            <div className="card">
              <div className="card-header"><span className="card-title">Report Details</span></div>
              <div className="card-body">
                {[
                  { label: 'Status', value: report.status },
                  { label: 'Version', value: `v${report.version}` },
                  { label: 'Confidence', value: report.confidence_score || '—' },
                  { label: 'Pipeline Run', value: <span className="mono">{report.pipeline_run_id.slice(0, 8)}...</span> },
                  { label: 'Generated', value: new Date(report.generated_at).toLocaleString() },
                  ...(report.approved_at ? [
                    { label: 'Approved At', value: new Date(report.approved_at).toLocaleString() },
                    { label: 'Approval Reason', value: report.approval_reason },
                  ] : []),
                ].map(({ label, value }) => (
                  <div key={label} style={{ display: 'flex', justifyContent: 'space-between', padding: '9px 0', borderBottom: '1px solid var(--border-subtle)', fontSize: 13 }}>
                    <span style={{ color: 'var(--text-muted)' }}>{label}</span>
                    <span style={{ fontWeight: 500, textAlign: 'right', maxWidth: 220 }}>{value}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'claims' && (
        <div className="fade-in">
          <p style={{ fontSize: 13.5, color: 'var(--text-secondary)', marginBottom: 16 }}>
            Each claim is grounded in evidence retrieved from submitted inputs. Click a claim to expand its citations.
          </p>
          {report.claims.sort((a, b) => a.display_order - b.display_order).map(claim => (
            <EvidencePanel key={claim.id} claim={claim} />
          ))}
          {report.claims.length === 0 && (
            <div className="empty-state"><div className="empty-title">No claims generated yet</div></div>
          )}
        </div>
      )}

      {activeTab === 'bias' && (
        <div className="fade-in">
          <p style={{ fontSize: 13.5, color: 'var(--text-secondary)', marginBottom: 16 }}>
            Bias flags are automatically detected by the Bias Detection Agent using dual-phase analysis.
          </p>
          {report.bias_flags.map(flag => (
            <div key={flag.id} className={`bias-flag ${flag.severity}`}>
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <span className={`badge ${flag.severity === 'HIGH' ? 'badge-red' : flag.severity === 'MEDIUM' ? 'badge-yellow' : 'badge-green'}`}>
                    {flag.severity}
                  </span>
                  <span style={{ fontWeight: 600, fontSize: 13.5 }}>{flag.bias_type}</span>
                </div>
                <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>
                  {new Date(flag.detected_at).toLocaleDateString()}
                </span>
              </div>
              {flag.affected_text && (
                <p className="citation-passage" style={{ margin: '8px 0' }}>"{flag.affected_text}"</p>
              )}
              <p style={{ fontSize: 13, color: 'var(--text-secondary)', marginBottom: 6 }}>
                <strong>Reasoning:</strong> {flag.detection_reasoning}
              </p>
              <p style={{ fontSize: 13, color: '#fcd34d' }}>
                <strong>Recommendation:</strong> {flag.recommended_action}
              </p>
            </div>
          ))}
          {report.bias_flags.length === 0 && (
            <div className="alert alert-success">
              <CheckCircle2 size={16} />
              No bias flags detected. The review inputs appear balanced and evidence-grounded.
            </div>
          )}
        </div>
      )}
    </div>
  )
}
