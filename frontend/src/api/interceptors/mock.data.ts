import type { UserRole } from '@/types';

export function getDemoDataForUrl(url: string, method: string): any {
  // Demo Employees
  if (url.includes('/users') && method === 'get') {
    if (url.match(/\/users\/[0-9a-f-]+$/)) {
      return {
        id: '1',
        email: 'alice.johnson@reviewguard.ai',
        full_name: 'Alice Johnson',
        role: 'EMPLOYEE',
        is_active: true,
        created_at: new Date().toISOString()
      };
    }
    return {
      items: [
        { id: '1', full_name: 'Alice Johnson', email: 'alice.j@reviewguard.ai', role: 'EMPLOYEE', is_active: true },
        { id: '2', full_name: 'Rahul Sharma', email: 'rahul.s@reviewguard.ai', role: 'EMPLOYEE', is_active: true },
        { id: '3', full_name: 'Emily Chen', email: 'emily.c@reviewguard.ai', role: 'EMPLOYEE', is_active: true },
        { id: '4', full_name: 'Michael Scott', email: 'michael.s@reviewguard.ai', role: 'MANAGER', is_active: true },
        { id: '5', full_name: 'Priya Singh', email: 'priya.s@reviewguard.ai', role: 'MANAGER', is_active: true }
      ],
      total: 5, skip: 0, limit: 100
    };
  }

  // Demo Review Cycles
  if (url.includes('/review-cycles') && method === 'get') {
    if (url.includes('/inputs')) {
      return [
        { id: 'input-1', input_type: 'self_assessment', content_text: 'Exceeded quarterly targets by 15%.', is_anonymized: false, submitted_at: new Date().toISOString() },
        { id: 'input-2', input_type: 'peer_feedback', content_text: 'Strong collaboration and leadership demonstrated in Q3.', is_anonymized: false, submitted_at: new Date().toISOString() }
      ];
    }
    
    if (url.match(/\/review-cycles\/[0-9a-f-]+$/)) {
      return {
        id: 'cycle-1',
        employee_id: '1',
        manager_id: '4',
        title: 'Q3 Performance Review',
        review_period_start: '2025-07-01T00:00:00Z',
        review_period_end: '2025-09-30T00:00:00Z',
        status: 'COMPLETED',
        created_at: new Date().toISOString()
      };
    }

    return {
      items: [
        {
          id: 'cycle-1', employee_id: '1', manager_id: '4', title: 'Q3 Performance Review',
          review_period_start: '2025-07-01T00:00:00Z', review_period_end: '2025-09-30T00:00:00Z',
          status: 'COMPLETED', created_at: new Date().toISOString()
        }
      ],
      total: 1, skip: 0, limit: 100
    };
  }

  // Demo Pipeline Status
  if (url.includes('/pipeline') && method === 'get') {
    return {
      pipeline_run_id: 'run-1',
      review_cycle_id: 'cycle-1',
      pipeline_status: 'COMPLETED',
      current_agent: 'Report Generation',
      agent_executions: [
        { agent_name: 'Extraction', status: 'COMPLETED', start_time: new Date().toISOString(), output_summary: 'Extracted text' },
        { agent_name: 'Performance Analysis', status: 'COMPLETED', start_time: new Date().toISOString(), output_summary: 'Performance claims generated' },
        { agent_name: 'Bias Detection', status: 'COMPLETED', start_time: new Date().toISOString(), output_summary: 'Low bias detected' },
        { agent_name: 'Explainability', status: 'COMPLETED', start_time: new Date().toISOString(), output_summary: 'Evidence linked' },
        { agent_name: 'Report Generation', status: 'COMPLETED', start_time: new Date().toISOString(), output_summary: 'Draft generated' }
      ]
    };
  }

  // Demo Reports
  if (url.includes('/reports') && method === 'get') {
    return {
      id: 'report-1',
      review_cycle_id: 'cycle-1',
      status: 'FINALIZED',
      executive_summary: 'Alice has demonstrated exceptional leadership and consistently exceeded her quarterly targets.',
      confidence_score: 'HIGH',
      confidence_explanation: 'Multiple peer reviews and metrics strongly corroborate the findings.',
      claims: [
        {
          id: 'claim-1', dimension: 'Performance', claim_text: 'Exceeded quarterly targets.',
          explanation: 'Verified through sales metrics and self-assessment.', confidence: 'HIGH',
          is_supported: true, display_order: 1,
          citations: [{ extracted_passage: 'Exceeded quarterly targets by 15%.', similarity_score: 0.95, retrieval_rank: 1 }]
        }
      ],
      bias_flags: [
        { id: 'bias-1', bias_type: 'RECENCY', severity: 'LOW', recommended_action: 'None', detection_reasoning: 'Minor emphasis on recent project, but balanced overall.', detected_at: new Date().toISOString() }
      ],
      generated_at: new Date().toISOString(),
      pipeline_run_id: 'run-1',
      version: 1
    };
  }

  // Fallback "No Data Available" empty state for arrays/objects
  if (url.includes('/audit')) return { items: [], total: 0 };
  
  // Default to empty object instead of crashing
  return {};
}
