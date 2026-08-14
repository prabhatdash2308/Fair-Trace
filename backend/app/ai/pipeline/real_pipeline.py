"""
FairTrace — Real Pipeline Executor
Bridges ReviewGuardState (TypedDict from pipeline_service.py) and
ReviewState (Pydantic model from agent classes).

Execution sequence:
  1. Build ReviewState from validated_inputs in ReviewGuardState
  2. Intake Agent  - normalizes inputs
  3. Evidence population - populate EvidenceState from available review inputs
     (skips Qdrant if not configured; uses text directly as citations)
  4. Bias Detection Agent - LLM bias scan
  5. Performance Analysis Agent - LLM analysis
  6. Explainability Agent - LLM trace
  7. Report Generation Agent - LLM report draft
  8. Persist Report, PerformanceClaims, BiasFlags, EvidenceCitations to DB
  9. Update ReviewGuardState with completion fields

All agents raise on failure. The caller (pipeline_service.execute_pipeline)
wraps this in try/except and updates pipeline_status=FAILED.
"""

import uuid
import structlog
from datetime import datetime, timezone

from app.ai.state.review_state import (
    ReviewState,
    MetadataState,
    InputState,
    EvidenceState,
    RetrievalState,
)

logger = structlog.get_logger(__name__)


class RealPipeline:
    """
    Synchronous pipeline executor.
    Accepts the ReviewGuardState dict (from pipeline_service) and
    returns an updated ReviewGuardState dict.
    """

    def __init__(
        self,
        intake_agent,
        bias_agent,
        analysis_agent,
        explainability_agent,
        report_agent,
    ):
        self.intake_agent = intake_agent
        self.bias_agent = bias_agent
        self.analysis_agent = analysis_agent
        self.explainability_agent = explainability_agent
        self.report_agent = report_agent

    def _build_review_state(self, guard_state: dict) -> ReviewState:
        meta = MetadataState(
            review_cycle_id=guard_state.get("review_cycle_id"),
            employee_id=guard_state.get("employee_id"),
            manager_id=guard_state.get("manager_id"),
            correlation_id=guard_state.get("correlation_id", guard_state["pipeline_run_id"]),
        )
        input_state = InputState()
        for vi in guard_state.get("validated_inputs", []):
            input_type = vi.get("input_type", "").upper()
            content = vi.get("content_text", "")
            if input_type == "SELF_ASSESSMENT":
                input_state.self_assessment = (input_state.self_assessment + "\n\n" + content).strip() if input_state.self_assessment else content
            elif input_type == "MANAGER_NOTE":
                input_state.manager_feedback = (input_state.manager_feedback + "\n\n" + content).strip() if input_state.manager_feedback else content
            elif input_type == "PEER_REVIEW":
                input_state.peer_feedback.append(content)
            elif input_type == "MEETING_NOTE":
                input_state.meeting_notes.append(content)
            elif input_type == "PROJECT_OUTCOME":
                input_state.project_outcomes.append(content)
            elif input_type == "GOAL":
                input_state.goals.append(content)
            else:
                input_state.uploaded_documents.append(content)
        return ReviewState(metadata=meta, input=input_state)

    def _populate_evidence_from_inputs(self, state: ReviewState) -> ReviewState:
        citations = []
        if state.input.self_assessment:
            citations.append(f"[Self Assessment] {state.input.self_assessment}")
        if state.input.manager_feedback:
            citations.append(f"[Manager Feedback] {state.input.manager_feedback}")
        for i, pf in enumerate(state.input.peer_feedback):
            citations.append(f"[Peer Feedback #{i+1}] {pf}")
        for i, mn in enumerate(state.input.meeting_notes):
            citations.append(f"[Meeting Note #{i+1}] {mn}")
        for i, po in enumerate(state.input.project_outcomes):
            citations.append(f"[Project Outcome #{i+1}] {po}")
        for i, g in enumerate(state.input.goals):
            citations.append(f"[Goal #{i+1}] {g}")
        state.evidence = EvidenceState(citations=citations, evidence_count=len(citations), status="completed")
        state.retrieval = RetrievalState(status="completed")
        return state

    def _record_agent_execution(self, guard_state, agent_name, status, output_summary, error_message=None, start_time=None):
        start = start_time or datetime.now(timezone.utc)
        end = datetime.now(timezone.utc)
        duration_ms = int((end - start).total_seconds() * 1000)
        
        record = {
            "agent_name": agent_name,
            "status": status,
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
            "output_summary": output_summary,
            "error_message": error_message,
            "items_processed": 0,
            "llm_model_used": None,
            "tokens_prompt": None,
            "tokens_completion": None,
            "tokens_total": None,
            "estimated_cost_usd": None,
            "latency_ms": duration_ms,
            "prompt_name": None,
            "prompt_version": None,
            "correlation_id": guard_state.get("correlation_id"),
            "llm_request_id": None,
        }
        guard_state.setdefault("agent_executions", []).append(record)

        # Persist to DB
        from core.database import SessionLocal
        from models.db.workflow import WorkflowExecution
        from models.db.agent_execution import AgentExecution, AgentStatus
        db = SessionLocal()
        try:
            workflow = db.query(WorkflowExecution).filter(
                WorkflowExecution.execution_id == guard_state["pipeline_run_id"]
            ).first()
            if workflow:
                seq = len(guard_state["agent_executions"])
                db_status = AgentStatus.COMPLETED if status == "COMPLETED" else AgentStatus.FAILED
                exec_record = AgentExecution(
                    workflow_execution_id=workflow.id,
                    agent_name=agent_name,
                    sequence=seq,
                    status=db_status,
                    started_at=start,
                    completed_at=end,
                    duration_ms=duration_ms,
                    error_message=error_message
                )
                db.add(exec_record)
                db.commit()
        except Exception as e:
            logger.error("failed_to_persist_agent_execution", error=str(e))
        finally:
            db.close()

    def _persist_report_to_db(self, state: ReviewState, guard_state: dict) -> str:
        from core.database import SessionLocal
        from models.db.report import Report
        from models.db.performance_claim import PerformanceClaim
        from models.db.bias_flag import BiasFlag
        from models.enums import ReportStatus, ConfidenceLevel, PerformanceDimension, BiasType as BiasTypeEnum, Severity
        from repositories.repositories import report_repo
        from models.db.review_cycle import ReviewCycle
        from models.enums import ReviewCycleStatus

        db = SessionLocal()
        try:
            review_cycle_id = uuid.UUID(guard_state["review_cycle_id"])
            pipeline_run_id = guard_state["pipeline_run_id"]
            confidence_numeric = getattr(state.analysis, "confidence_score", 0.0)
            if confidence_numeric >= 70:
                conf_level = ConfidenceLevel.HIGH
            elif confidence_numeric >= 50:
                conf_level = ConfidenceLevel.MEDIUM
            elif confidence_numeric >= 30:
                conf_level = ConfidenceLevel.LOW
            else:
                conf_level = ConfidenceLevel.INSUFFICIENT

            report_repo.mark_previous_not_current(db, review_cycle_id)

            report = Report(
                review_cycle_id=review_cycle_id,
                version=1,
                status=ReportStatus.PENDING_APPROVAL,
                executive_summary=state.report.executive_summary or state.report.performance_summary,
                recommended_actions=state.report.recommendations,
                confidence_score=conf_level,
                confidence_explanation=state.report.confidence_summary or "",
                pipeline_run_id=pipeline_run_id,
                is_current=True,
            )
            db.add(report)
            db.flush()
            report_id = report.id

            # Save EvidenceCitations linked to ReviewInputs
            from models.db.evidence_citation import EvidenceCitation
            if "validated_inputs" in guard_state:
                for vi in guard_state["validated_inputs"]:
                    db.add(EvidenceCitation(
                        review_input_id=uuid.UUID(vi["input_id"]),
                        source_type=vi["input_type"],
                        extracted_passage=vi["content_text"][:500], # Keep a snippet
                        similarity_score=1.0,
                        retrieval_rank=1,
                    ))
            db.flush()

            dimension_map = {
                "technical": PerformanceDimension.TECHNICAL,
                "collaboration": PerformanceDimension.COLLABORATION,
                "leadership": PerformanceDimension.LEADERSHIP,
                "delivery": PerformanceDimension.DELIVERY,
                "growth": PerformanceDimension.GROWTH,
            }
            display_order = 0
            for strength in state.analysis.strengths:
                db.add(PerformanceClaim(
                    report_id=report_id,
                    dimension=PerformanceDimension.TECHNICAL,
                    claim_text=strength,
                    explanation="Identified strength from evidence analysis.",
                    confidence=conf_level,
                    is_supported=True,
                    display_order=display_order,
                ))
                display_order += 1

            for competency_name, score in state.analysis.competencies.items():
                dimension = dimension_map.get(competency_name.lower(), PerformanceDimension.TECHNICAL)
                
                # Fetch detailed explanation from the explainability trace if available
                explanation_trace = f"Score: {score:.1f}"
                if hasattr(state, 'explainability') and state.explainability.competency_explanations:
                    trace = state.explainability.competency_explanations.get(competency_name)
                    if trace:
                        explanation_trace = trace
                        
                db.add(PerformanceClaim(
                    report_id=report_id,
                    dimension=dimension,
                    claim_text=f"{competency_name}: {score:.0f}/100",
                    explanation=explanation_trace,
                    confidence=conf_level,
                    is_supported=True,
                    display_order=display_order,
                ))
                display_order += 1

            bias_type_map = {
                "RECENCY": BiasTypeEnum.RECENCY, "HALO": BiasTypeEnum.HALO,
                "HORN": BiasTypeEnum.HORN, "LENIENCY": BiasTypeEnum.LENIENCY,
                "SEVERITY": BiasTypeEnum.SEVERITY, "UNSUPPORTED": BiasTypeEnum.UNSUPPORTED,
                "IMBALANCE": BiasTypeEnum.IMBALANCE, "GENDER": BiasTypeEnum.UNSUPPORTED,
                "AGE": BiasTypeEnum.UNSUPPORTED,
            }
            severity_map = {"LOW": Severity.LOW, "MEDIUM": Severity.MEDIUM, "HIGH": Severity.HIGH}
            for finding in state.bias.findings:
                bias_type_str = finding.bias_type.name if hasattr(finding.bias_type, "name") else str(finding.bias_type)
                severity_str = finding.severity.name if hasattr(finding.severity, "name") else str(finding.severity)
                db.add(BiasFlag(
                    report_id=report_id,
                    bias_type=bias_type_map.get(bias_type_str.upper(), BiasTypeEnum.UNSUPPORTED),
                    severity=severity_map.get(severity_str.upper(), Severity.MEDIUM),
                    recommended_action=finding.recommendation,
                    detected_by_agent="BiasDetectionAgent",
                    detection_reasoning=finding.reason,
                ))

            db.commit()
            db.refresh(report)

            cycle = db.get(ReviewCycle, review_cycle_id)
            if cycle:
                cycle.status = ReviewCycleStatus.PENDING_APPROVAL
                db.commit()

            logger.info("report_persisted_to_db", report_id=str(report_id), pipeline_run_id=pipeline_run_id)
            return str(report_id)
        except Exception as exc:
            db.rollback()
            logger.error("report_persist_failed", error=str(exc))
            raise
        finally:
            db.close()

    def invoke(self, guard_state: dict) -> dict:
        pipeline_run_id = guard_state["pipeline_run_id"]
        log = logger.bind(pipeline_run_id=pipeline_run_id)
        log.info("real_pipeline_start")

        # Step 0: Load review inputs from DB
        log.info("loading_db_inputs")
        try:
            from core.database import SessionLocal
            from repositories.repositories import review_input_repo
            import uuid as _uuid
            db = SessionLocal()
            try:
                cycle_id = _uuid.UUID(guard_state["review_cycle_id"])
                db_inputs = review_input_repo.list_for_cycle(db, cycle_id)
                validated_inputs = [{
                    "input_id": str(inp.id),
                    "input_type": inp.input_type.value,
                    "content_text": inp.content_text,
                    "submitted_by_id": str(inp.submitted_by),
                    "submitted_at": inp.submitted_at.isoformat(),
                    "is_anonymized": inp.is_anonymized,
                    "char_count": len(inp.content_text),
                    "submission_week": inp.submitted_at.isocalendar()[1],
                } for inp in db_inputs]
                guard_state["validated_inputs"] = validated_inputs
                guard_state["raw_input_ids"] = [v["input_id"] for v in validated_inputs]
            finally:
                db.close()
        except Exception as exc:
            log.error("db_load_failed", error=str(exc))
            guard_state["pipeline_status"] = "FAILED"
            guard_state["error_state"] = {"agent": "db_loader", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
            return guard_state

        log.info("inputs_loaded", count=len(guard_state["validated_inputs"]))

        # Step 1: Build ReviewState
        state = self._build_review_state(guard_state)

        # Step 2: Intake Agent
        guard_state["current_agent"] = "IntakeAgent"
        start_time = datetime.now(timezone.utc)
        try:
            state = self.intake_agent.execute(state)
            guard_state["intake_complete"] = True
            self._record_agent_execution(guard_state, "IntakeAgent", "COMPLETED", f"Processed {len(validated_inputs)} inputs.", start_time=start_time)
        except Exception as exc:
            log.warning("intake_failed_continuing", error=str(exc))
            self._record_agent_execution(guard_state, "IntakeAgent", "FAILED", "", error_message=str(exc), start_time=start_time)

        # Step 3: Evidence Population
        guard_state["current_agent"] = "EvidenceAgent"
        start_time = datetime.now(timezone.utc)
        try:
            state = self._populate_evidence_from_inputs(state)
            guard_state["evidence_ready"] = True
            guard_state["embedding_complete"] = True
            self._record_agent_execution(guard_state, "EvidenceAgent", "COMPLETED", f"Populated {state.evidence.evidence_count} citations.", start_time=start_time)
        except Exception as exc:
            log.error("evidence_failed", error=str(exc))
            guard_state["pipeline_status"] = "FAILED"
            guard_state["error_state"] = {"agent": "EvidenceAgent", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
            self._record_agent_execution(guard_state, "EvidenceAgent", "FAILED", "", error_message=str(exc), start_time=start_time)
            return guard_state

        # Step 4: Bias Detection Agent
        guard_state["current_agent"] = "BiasDetectionAgent"
        start_time = datetime.now(timezone.utc)
        try:
            state = self.bias_agent.execute(state)
            guard_state["bias_detection_complete"] = True
            guard_state["high_bias_count"] = sum(1 for f in state.bias.findings if hasattr(f.severity, "name") and f.severity.name == "HIGH")
            guard_state["medium_bias_count"] = sum(1 for f in state.bias.findings if hasattr(f.severity, "name") and f.severity.name == "MEDIUM")
            self._record_agent_execution(guard_state, "BiasDetectionAgent", "COMPLETED", f"Detected {len(state.bias.findings)} bias flags.", start_time=start_time)
        except Exception as exc:
            log.warning("bias_failed_continuing", error=str(exc))
            state.bias.status = "completed"
            self._record_agent_execution(guard_state, "BiasDetectionAgent", "FAILED", "", error_message=str(exc), start_time=start_time)

        # Step 5: Performance Analysis Agent
        guard_state["current_agent"] = "PerformanceAnalysisAgent"
        start_time = datetime.now(timezone.utc)
        try:
            state = self.analysis_agent.execute(state)
            guard_state["analysis_complete"] = True
            self._record_agent_execution(guard_state, "PerformanceAnalysisAgent", "COMPLETED", f"Analysis complete. Confidence: {state.analysis.confidence_score:.1f}%", start_time=start_time)
        except Exception as exc:
            log.error("analysis_failed", error=str(exc))
            guard_state["pipeline_status"] = "FAILED"
            guard_state["error_state"] = {"agent": "PerformanceAnalysisAgent", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
            self._record_agent_execution(guard_state, "PerformanceAnalysisAgent", "FAILED", "", error_message=str(exc), start_time=start_time)
            return guard_state

        # Step 6: Explainability Agent
        guard_state["current_agent"] = "ExplainabilityAgent"
        start_time = datetime.now(timezone.utc)
        try:
            state = self.explainability_agent.execute(state)
            guard_state["explainability_complete"] = True
            self._record_agent_execution(guard_state, "ExplainabilityAgent", "COMPLETED", f"Generated {len(state.explainability.decision_path)} reasoning steps.", start_time=start_time)
        except Exception as exc:
            log.warning("explainability_failed_continuing", error=str(exc))
            state.explainability.status = "completed"
            self._record_agent_execution(guard_state, "ExplainabilityAgent", "FAILED", "", error_message=str(exc), start_time=start_time)

        # Step 7: Report Generation Agent
        guard_state["current_agent"] = "ReportGenerationAgent"
        start_time = datetime.now(timezone.utc)
        try:
            state = self.report_agent.execute(state)
            guard_state["report_complete"] = True
            guard_state["executive_summary"] = state.report.executive_summary
            guard_state["recommended_actions"] = state.report.recommendations
            self._record_agent_execution(guard_state, "ReportGenerationAgent", "COMPLETED", "Report draft generated.", start_time=start_time)
        except Exception as exc:
            log.error("report_agent_failed", error=str(exc))
            guard_state["pipeline_status"] = "FAILED"
            guard_state["error_state"] = {"agent": "ReportGenerationAgent", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
            self._record_agent_execution(guard_state, "ReportGenerationAgent", "FAILED", "", error_message=str(exc), start_time=start_time)
            return guard_state

        # Step 8: Persist to DB
        guard_state["current_agent"] = "DBPersistence"
        start_time = datetime.now(timezone.utc)
        try:
            report_db_id = self._persist_report_to_db(state, guard_state)
            guard_state["report_db_id"] = report_db_id
            self._record_agent_execution(guard_state, "DBPersistence", "COMPLETED", f"Report persisted. ID: {report_db_id}", start_time=start_time)
        except Exception as exc:
            log.error("db_persistence_failed", error=str(exc))
            guard_state["pipeline_status"] = "FAILED"
            guard_state["error_state"] = {"agent": "DBPersistence", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
            self._record_agent_execution(guard_state, "DBPersistence", "FAILED", "", error_message=str(exc), start_time=start_time)
            return guard_state

        # Complete
        guard_state["pipeline_status"] = "COMPLETED"
        guard_state["current_agent"] = "completed"
        guard_state["completed_at"] = datetime.now(timezone.utc).isoformat()
        guard_state["approval_required"] = True
        guard_state["approval_status"] = "PENDING"
        log.info("real_pipeline_completed", report_db_id=guard_state.get("report_db_id"))
        return guard_state
