# Phase 11.11: Enterprise Human Approval Workflow

## Overview
This phase introduces Human-in-the-Loop (HITL) review on top of the completed LangGraph AI pipeline. The workflow pauses execution precisely after the `ReportNode` finishes generating the `EnterprisePerformanceReportSchema`.

## Architecture Details

### 1. State Machine transitions
We abstracted a robust state machine independent from the AI logic.
- **WorkflowStatus**: `RUNNING` -> `WAITING_APPROVAL` -> `APPROVED` / `REJECTED` / `REVISION_REQUESTED`
- **ApprovalStatus**: Tracks the exact state of the reviewer decision loop.

### 2. LangGraph Interrupts
The LangGraph pipeline compiles with the custom `ApprovalNode`. Upon reaching this node, the node executes a `raise NodeInterrupt("waiting for approval")` to immediately halt the state thread without completing the graph.

### 3. Checkpointing & Resume
The `WorkflowService` triggers `resume_workflow()` when a reviewer submits a `POST /decision`. This clears the waiting state and will allow the LangGraph instance to continue through its final conditional edge.

### 4. Telemetry & History
All decisions are entirely immutable and logged via:
- `HistoryService.log_event` (persists detailed workflow status tracking)
- `AuditService.audit_decision` (captures reviewer ID, explicit comments, and a snapshot of state for complete transparency)
- `NotificationProvider` interface, allowing enterprise connections (Email, Slack, MS Teams) over time.

This phase wraps the pure AI steps (Performance, Bias, Explainability, Report) into a compliant, business-ready approval pipeline.
