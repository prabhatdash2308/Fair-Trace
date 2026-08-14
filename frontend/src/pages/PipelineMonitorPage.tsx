import React, { useEffect, useRef, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { CheckCircle, XCircle, Clock, AlertTriangle, Activity, DollarSign, Cpu, RefreshCw } from 'lucide-react'
import { cyclesApi, pipelineApi, type PipelineStatus, type AgentExecution } from '../api'
import { useAuthStore } from '../store'

const AGENT_LABELS: Record<string, string> = {
  intake_agent: '1. Intake',
  embedding_agent: '2. Embedding',
  evidence_retrieval_agent: '3. Evidence Retrieval',
  bias_detection_agent: '4. Bias Detection',
  performance_analysis_agent: '5. Performance Analysis',
  report_generation_agent: '6. Report Generation',
  explainability_agent: '7. Explainability',
  human_approval_agent: '8. Human Approval',
  finalization_agent: '9. Finalization',
}

const ALL_AGENTS = Object.keys(AGENT_LABELS)

function AgentStep({ agent, execution }: { agent: string; execution?: AgentExecution }) {
  const status = execution?.status?.toLowerCase() || 'pending'
  const isRunning = status === 'success' ? false : execution && !execution.end_time
  const effectiveStatus = isRunning ? 'running' : status

  return (
    <div className={`pipeline-step ${effectiveStatus}`}>
      <div className={`step-dot ${effectiveStatus}`} />
      <div style={{ flex: 1 }}>
        <div className="flex items-center justify-between">
          <span style={{ fontSize: 13, fontWeight: 500 }}>{AGENT_LABELS[agent] || agent}</span>
          <div className="flex items-center gap-2">
            {execution?.latency_ms && (
              <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>{execution.latency_ms}ms</span>
            )}
            {execution?.tokens_total && (
              <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>{execution.tokens_total} tok</span>
            )}
            {effectiveStatus === 'running' && <span className="spinner" style={{ width: 12, height: 12, borderWidth: 1.5 }} />}
            {effectiveStatus === 'success' && <CheckCircle size={14} color="#10b981" />}
            {effectiveStatus === 'failure' && <XCircle size={14} color="#ef4444" />}
            {effectiveStatus === 'pending' && <Clock size={14} color="var(--text-muted)" />}
          </div>
        </div>
        {execution?.output_summary && (
          <p style={{ fontSize: 11.5, color: 'var(--text-secondary)', marginTop: 3, lineHeight: 1.4 }}>
            {execution.output_summary}
          </p>
        )}
        {execution?.error_message && (
          <p style={{ fontSize: 11.5, color: '#fca5a5', marginTop: 3 }}>
            ⚠ {execution.error_message}
          </p>
        )}
      </div>
    </div>
  )
}

export default function PipelineMonitorPage() {
  const { cycleId } = useParams()
  const navigate = useNavigate()
  const { user } = useAuthStore()

  const [runId, setRunId] = useState<string | null>(null)
  const [status, setStatus] = useState<PipelineStatus | null>(null)
  const [triggering, setTriggering] = useState(false)
  const [error, setError] = useState('')
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null)

  const isTerminal = (s: string) =>
    ['COMPLETED', 'FAILED', 'HALTED', 'AWAITING_HUMAN'].includes(s)

  const poll = async (id: string) => {
    try {
      const data = await pipelineApi.getStatus(id)
      setStatus(data)
      if (isTerminal(data.pipeline_status)) {
        if (pollRef.current) clearInterval(pollRef.current)
      }
    } catch { }
  }

  useEffect(() => {
    return () => { if (pollRef.current) clearInterval(pollRef.current) }
  }, [])

  const triggerPipeline = async () => {
    if (!cycleId) return
    setTriggering(true)
    setError('')
    try {
      const res = await cyclesApi.triggerPipeline(cycleId)
      setRunId(res.pipeline_run_id)
      pollRef.current = setInterval(() => poll(res.pipeline_run_id), 2000)
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to trigger pipeline')
    } finally {
      setTriggering(false)
    }
  }

  const executionMap = status?.agent_executions.reduce((acc, e) => {
    acc[e.agent_name] = e
    return acc
  }, {} as Record<string, AgentExecution>) || {}

  return (
    <div className="fade-in">
      <div className="page-header">
        <button onClick={() => navigate(`/cycles/${cycleId}`)}
          style={{ fontSize: 12.5, color: 'var(--text-muted)', background: 'none', border: 'none', cursor: 'pointer', marginBottom: 12 }}>
          ← Back to Cycle
        </button>
        <h1 className="page-title">AI Pipeline Monitor</h1>
        <p className="page-subtitle">Real-time execution of the 9-agent FairTrace pipeline</p>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      <div className="grid-2" style={{ gap: 24 }}>
        {/* Left: Agent Steps */}
        <div>
          <div className="card">
            <div className="card-header">
              <span className="card-title">Agent Execution</span>
              {status && (
                <span className={`badge ${
                  status.pipeline_status === 'COMPLETED' ? 'badge-green' :
                  status.pipeline_status === 'FAILED' ? 'badge-red' :
                  status.pipeline_status === 'AWAITING_HUMAN' ? 'badge-yellow' :
                  'badge-blue'
                }`}>
                  {status.pipeline_status}
                </span>
              )}
            </div>
            <div className="card-body" style={{ paddingTop: 16 }}>
              {ALL_AGENTS.map(agent => (
                <AgentStep key={agent} agent={agent} execution={executionMap[agent]} />
              ))}
            </div>
          </div>

          {!runId && (
            <button
              className="btn btn-primary"
              style={{ width: '100%', justifyContent: 'center', marginTop: 16, padding: 14 }}
              onClick={triggerPipeline}
              disabled={triggering}
            >
              {triggering ? <><span className="spinner" /> Triggering...</> : '⚡ Trigger AI Pipeline'}
            </button>
          )}
        </div>

        {/* Right: Metrics + Status */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          {status && (
            <>
              {/* Cost metrics */}
              <div className="grid-2" style={{ gap: 12 }}>
                <div className="stat-card" style={{ padding: 16 }}>
                  <div className="stat-label"><Cpu size={11} style={{ display: 'inline', marginRight: 4 }} />Tokens Used</div>
                  <div className="stat-value" style={{ fontSize: 24 }}>
                    {(status.pipeline_total_tokens || 0).toLocaleString()}
                  </div>
                </div>
                <div className="stat-card" style={{ padding: 16 }}>
                  <div className="stat-label"><DollarSign size={11} style={{ display: 'inline', marginRight: 4 }} />Est. Cost</div>
                  <div className="stat-value" style={{ fontSize: 24 }}>
                    ${(status.pipeline_total_cost_usd || 0).toFixed(4)}
                  </div>
                </div>
              </div>

              {/* Agent detail table */}
              <div className="card">
                <div className="card-header">
                  <span className="card-title">Agent Metrics</span>
                </div>
                <div className="table-container" style={{ border: 'none', borderRadius: 0 }}>
                  <table>
                    <thead>
                      <tr>
                        <th>Agent</th>
                        <th>Latency</th>
                        <th>Tokens</th>
                        <th>Cost</th>
                      </tr>
                    </thead>
                    <tbody>
                      {status.agent_executions.map(ex => (
                        <tr key={ex.agent_name}>
                          <td style={{ fontSize: 12 }}>{AGENT_LABELS[ex.agent_name] || ex.agent_name}</td>
                          <td style={{ fontSize: 12, fontFamily: 'var(--font-mono)' }}>
                            {ex.latency_ms ? `${ex.latency_ms}ms` : '—'}
                          </td>
                          <td style={{ fontSize: 12, fontFamily: 'var(--font-mono)' }}>
                            {ex.tokens_total?.toLocaleString() || '—'}
                          </td>
                          <td style={{ fontSize: 12, fontFamily: 'var(--font-mono)' }}>
                            {ex.estimated_cost_usd ? `$${ex.estimated_cost_usd.toFixed(5)}` : '—'}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Navigation after completion */}
              {status.pipeline_status === 'AWAITING_HUMAN' && (
                <div className="alert alert-warning">
                  <AlertTriangle size={16} />
                  <div>
                    <strong>Report ready for review.</strong> The AI pipeline has completed and the report is now pending your approval.
                    <button className="btn btn-sm btn-primary" style={{ marginTop: 8, display: 'block' }}
                      onClick={() => navigate(`/cycles/${cycleId}`)}>
                      View Report
                    </button>
                  </div>
                </div>
              )}

              {status.pipeline_status === 'FAILED' && status.error_state && (
                <div className="alert alert-error">
                  <XCircle size={16} />
                  <div>
                    <strong>Pipeline failed:</strong> {(status.error_state as any).error || 'Unknown error'}
                  </div>
                </div>
              )}
            </>
          )}

          {!status && !triggering && (
            <div className="card" style={{ textAlign: 'center', padding: '40px 24px' }}>
              <Activity size={40} color="var(--text-muted)" style={{ margin: '0 auto 12px' }} />
              <p style={{ color: 'var(--text-secondary)', fontSize: 14 }}>
                Click "Trigger AI Pipeline" to start the 9-agent analysis
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
