"""Initial migration — create all enum types and tables.

Revision ID: 0001
Revises:
Create Date: 2026-08-01

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── Enum Types ──────────────────────────────────────────────────────────────
    user_role = postgresql.ENUM(
        "ADMIN", "MANAGER", "EMPLOYEE", name="user_role", create_type=False
    )
    user_role.create(op.get_bind(), checkfirst=True)

    review_cycle_status = postgresql.ENUM(
        "DRAFT", "ACTIVE", "PROCESSING", "PENDING_APPROVAL", "COMPLETED", "CANCELLED",
        name="review_cycle_status", create_type=False,
    )
    review_cycle_status.create(op.get_bind(), checkfirst=True)

    report_status = postgresql.ENUM(
        "DRAFT", "PENDING_APPROVAL", "FINALIZED", "REVISION_REQUESTED", "REJECTED",
        name="report_status", create_type=False,
    )
    report_status.create(op.get_bind(), checkfirst=True)

    input_type = postgresql.ENUM(
        "SELF_ASSESSMENT", "MANAGER_NOTE", "PEER_REVIEW",
        "PROJECT_OUTCOME", "GOAL", "MEETING_NOTE",
        name="input_type", create_type=False,
    )
    input_type.create(op.get_bind(), checkfirst=True)

    performance_dimension = postgresql.ENUM(
        "TECHNICAL", "COLLABORATION", "LEADERSHIP", "DELIVERY", "GROWTH",
        name="performance_dimension", create_type=False,
    )
    performance_dimension.create(op.get_bind(), checkfirst=True)

    bias_type = postgresql.ENUM(
        "RECENCY", "HALO", "HORN", "LENIENCY", "SEVERITY", "UNSUPPORTED", "IMBALANCE",
        name="bias_type", create_type=False,
    )
    bias_type.create(op.get_bind(), checkfirst=True)

    severity = postgresql.ENUM(
        "HIGH", "MEDIUM", "LOW", name="severity", create_type=False
    )
    severity.create(op.get_bind(), checkfirst=True)

    confidence_level = postgresql.ENUM(
        "HIGH", "MEDIUM", "LOW", "INSUFFICIENT", name="confidence_level", create_type=False
    )
    confidence_level.create(op.get_bind(), checkfirst=True)

    audit_event_type = postgresql.ENUM(
        "REVIEW_CYCLE_CREATED", "REVIEW_CYCLE_UPDATED", "REVIEW_CYCLE_CANCELLED",
        "INPUT_SUBMITTED", "PIPELINE_TRIGGERED", "PIPELINE_COMPLETED", "PIPELINE_FAILED",
        "AGENT_EXECUTED", "REPORT_GENERATED", "REPORT_APPROVED", "REPORT_REJECTED",
        "REPORT_REVISION_REQUESTED", "USER_LOGIN", "USER_LOGOUT", "ACCESS_DENIED",
        name="audit_event_type", create_type=False,
    )
    audit_event_type.create(op.get_bind(), checkfirst=True)

    # ── Tables ──────────────────────────────────────────────────────────────────
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("role", user_role, nullable=False),
        sa.Column("manager_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("idx_users_email", "users", ["email"], unique=True)

    op.create_table(
        "review_cycles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("employee_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("manager_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("review_period_start", sa.Date, nullable=False),
        sa.Column("review_period_end", sa.Date, nullable=False),
        sa.Column("status", review_cycle_status, nullable=False, server_default="DRAFT"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("idx_review_cycles_employee", "review_cycles", ["employee_id"])
    op.create_index("idx_review_cycles_manager", "review_cycles", ["manager_id"])
    op.create_index("idx_review_cycles_status", "review_cycles", ["status"])

    op.create_table(
        "review_inputs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("review_cycle_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("review_cycles.id"), nullable=False),
        sa.Column("submitted_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("input_type", input_type, nullable=False),
        sa.Column("content_text", sa.Text, nullable=False),
        sa.Column("is_anonymized", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("submitted_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("qdrant_document_id", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("idx_review_inputs_cycle", "review_inputs", ["review_cycle_id"])
    op.create_index("idx_review_inputs_type", "review_inputs", ["input_type"])

    op.create_table(
        "reports",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("review_cycle_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("review_cycles.id"), nullable=False),
        sa.Column("version", sa.Integer, nullable=False, server_default="1"),
        sa.Column("status", report_status, nullable=False, server_default="DRAFT"),
        sa.Column("executive_summary", sa.Text, nullable=True),
        sa.Column("recommended_actions", postgresql.JSONB, nullable=True),
        sa.Column("confidence_score", confidence_level, nullable=True),
        sa.Column("confidence_explanation", sa.Text, nullable=True),
        sa.Column("approved_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("approval_reason", sa.Text, nullable=True),
        sa.Column("pipeline_run_id", sa.String(255), nullable=False),
        sa.Column("is_current", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("generated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("approval_idempotency_key", sa.String(255), nullable=True, unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("idx_reports_cycle", "reports", ["review_cycle_id"])
    op.create_index("idx_reports_status", "reports", ["status"])
    op.create_index("idx_reports_pipeline", "reports", ["pipeline_run_id"])
    op.create_index("idx_reports_current", "reports", ["is_current"])

    op.create_table(
        "performance_claims",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("report_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("reports.id"), nullable=False),
        sa.Column("dimension", performance_dimension, nullable=False),
        sa.Column("claim_text", sa.Text, nullable=False),
        sa.Column("explanation", sa.Text, nullable=False, server_default=""),
        sa.Column("confidence", confidence_level, nullable=False),
        sa.Column("is_supported", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("display_order", sa.Integer, nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("idx_claims_report", "performance_claims", ["report_id"])
    op.create_index("idx_claims_dimension", "performance_claims", ["dimension"])

    op.create_table(
        "evidence_citations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("claim_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("performance_claims.id"), nullable=False),
        sa.Column("review_input_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("review_inputs.id"), nullable=False),
        sa.Column("extracted_passage", sa.Text, nullable=False),
        sa.Column("similarity_score", sa.Float, nullable=False),
        sa.Column("retrieval_rank", sa.Integer, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("idx_citations_claim", "evidence_citations", ["claim_id"])
    op.create_index("idx_citations_input", "evidence_citations", ["review_input_id"])

    op.create_table(
        "bias_flags",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("report_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("reports.id"), nullable=False),
        sa.Column("review_input_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("review_inputs.id"), nullable=True),
        sa.Column("bias_type", bias_type, nullable=False),
        sa.Column("severity", severity, nullable=False),
        sa.Column("affected_text", sa.Text, nullable=True),
        sa.Column("recommended_action", sa.Text, nullable=False),
        sa.Column("detected_by_agent", sa.String(100), nullable=False),
        sa.Column("detection_reasoning", sa.Text, nullable=False),
        sa.Column("detected_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("idx_bias_flags_report", "bias_flags", ["report_id"])
    op.create_index("idx_bias_flags_type", "bias_flags", ["bias_type"])
    op.create_index("idx_bias_flags_severity", "bias_flags", ["severity"])

    op.create_table(
        "audit_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("event_type", audit_event_type, nullable=False),
        sa.Column("actor_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("actor_role", user_role, nullable=True),
        sa.Column("resource_type", sa.String(100), nullable=False),
        sa.Column("resource_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("event_payload", postgresql.JSONB, nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("correlation_id", sa.String(255), nullable=True),
        sa.Column("state_version", sa.Integer, nullable=True),
        sa.Column("prompt_version", sa.String(50), nullable=True),
    )
    op.create_index("idx_audit_event_type", "audit_events", ["event_type"])
    op.create_index("idx_audit_resource", "audit_events", ["resource_id"])
    op.create_index("idx_audit_occurred", "audit_events", ["occurred_at"])
    op.create_index("idx_audit_correlation", "audit_events", ["correlation_id"])


def downgrade() -> None:
    op.drop_table("audit_events")
    op.drop_table("bias_flags")
    op.drop_table("evidence_citations")
    op.drop_table("performance_claims")
    op.drop_table("reports")
    op.drop_table("review_inputs")
    op.drop_table("review_cycles")
    op.drop_table("users")

    # Drop enum types in reverse dependency order
    for enum_name in [
        "audit_event_type", "confidence_level", "severity", "bias_type",
        "performance_dimension", "input_type", "report_status",
        "review_cycle_status", "user_role",
    ]:
        op.execute(f"DROP TYPE IF EXISTS {enum_name}")
