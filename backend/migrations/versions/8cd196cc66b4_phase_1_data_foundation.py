"""Phase 1 Data Foundation

Revision ID: 8cd196cc66b4
Revises: bdc668b44ec3
Create Date: 2026-08-14 04:31:37.283214+00:00

"""
from typing import Sequence, Union
import uuid
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8cd196cc66b4'
down_revision: Union[str, None] = 'bdc668b44ec3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Rename table review_cycles -> reviews
    op.rename_table('review_cycles', 'reviews')
    
    # Rename old indexes that conflict
    op.execute("ALTER INDEX IF EXISTS ix_review_cycles_organization_id RENAME TO ix_reviews_organization_id")
    op.execute("ALTER INDEX IF EXISTS ix_review_cycles_status RENAME TO ix_reviews_status_old")
    op.execute("ALTER INDEX IF EXISTS ix_review_cycles_employee_id RENAME TO ix_reviews_employee_id")
    op.execute("ALTER INDEX IF EXISTS ix_review_cycles_manager_id RENAME TO ix_reviews_manager_id")
    
    # 2. Rename dependent columns
    op.alter_column('reports', 'review_cycle_id', new_column_name='review_id')
    op.alter_column('review_inputs', 'review_cycle_id', new_column_name='review_id')
    op.alter_column('workflow_executions', 'review_cycle_id', new_column_name='review_id')

    # Drop old constraints and create new ones for reviews
    op.drop_constraint('reports_review_cycle_id_fkey', 'reports', type_='foreignkey')
    op.create_foreign_key('reports_review_id_fkey', 'reports', 'reviews', ['review_id'], ['id'])
    
    op.drop_constraint('review_inputs_review_cycle_id_fkey', 'review_inputs', type_='foreignkey')
    op.create_foreign_key('review_inputs_review_id_fkey', 'review_inputs', 'reviews', ['review_id'], ['id'])
    
    op.drop_constraint('workflow_executions_review_cycle_id_fkey', 'workflow_executions', type_='foreignkey')
    op.create_foreign_key('workflow_executions_review_id_fkey', 'workflow_executions', 'reviews', ['review_id'], ['id'])

    # Drop old indexes and create new ones
    op.drop_index('ix_reports_review_cycle_id', table_name='reports')
    op.create_index(op.f('ix_reports_review_id'), 'reports', ['review_id'], unique=False)
    
    op.drop_index('ix_review_inputs_review_cycle_id', table_name='review_inputs')
    op.create_index(op.f('ix_review_inputs_review_id'), 'review_inputs', ['review_id'], unique=False)

    op.drop_index('uq_active_workflow_per_cycle', table_name='workflow_executions', postgresql_where="(status = 'RUNNING'::workflowstatus)")
    op.create_index('uq_active_workflow_per_review', 'workflow_executions', ['review_id'], unique=True, postgresql_where=sa.text("status = 'RUNNING'"))

    # 3. Create NEW review_cycles table
    op.create_table('review_cycles',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('created_by', sa.UUID(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('status', postgresql.ENUM('DRAFT', 'ACTIVE', 'COMPLETED', 'CANCELLED', name='review_cycle_status', create_type=False), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_review_cycles_organization_id'), 'review_cycles', ['organization_id'], unique=False)
    op.create_index(op.f('ix_review_cycles_status'), 'review_cycles', ['status'], unique=False)

    # Add review_cycle_id to reviews, temporarily nullable
    op.add_column('reviews', sa.Column('review_cycle_id', sa.UUID(), nullable=True))

    # 4. Data Migration: Create legacy cycles per organization and assign reviews
    connection = op.get_bind()
    
    # Get all distinct organizations that have reviews
    orgs = connection.execute(sa.text("SELECT DISTINCT organization_id FROM reviews WHERE organization_id IS NOT NULL")).fetchall()
    
    for org in orgs:
        org_id = org[0]
        # Get an admin or user to be creator
        user = connection.execute(sa.text(f"SELECT id FROM users WHERE organization_id = '{org_id}' LIMIT 1")).fetchone()
        creator_id = user[0] if user else uuid.uuid4() # Fallback if somehow no user
        
        cycle_id = uuid.uuid4()
        connection.execute(sa.text(f"""
            INSERT INTO review_cycles (id, organization_id, created_by, title, start_date, end_date, status, created_at, updated_at)
            VALUES ('{cycle_id}', '{org_id}', '{creator_id}', 'Legacy Reviews - Imported', CURRENT_DATE, CURRENT_DATE, 'COMPLETED', NOW(), NOW())
        """))
        
        # Backfill
        connection.execute(sa.text(f"""
            UPDATE reviews SET review_cycle_id = '{cycle_id}' WHERE organization_id = '{org_id}'
        """))

    # For any reviews without org_id, assign to a generic legacy cycle or throw.
    # The architecture assumes everything is tied to an org. If org is null, we can't reliably create a Legacy Cycle for it that's org-isolated.
    # We will throw if there are any to enforce integrity.
    null_org_reviews = connection.execute(sa.text("SELECT COUNT(*) FROM reviews WHERE organization_id IS NULL OR review_cycle_id IS NULL")).scalar()
    if null_org_reviews > 0:
        raise Exception("Found reviews without organization_id. Cannot migrate cleanly without an organization context.")

    # 5. Make review_cycle_id NOT NULL
    op.alter_column('reviews', 'review_cycle_id', nullable=False)
    op.create_foreign_key('reviews_review_cycle_id_fkey', 'reviews', 'review_cycles', ['review_cycle_id'], ['id'])
    op.create_index(op.f('ix_reviews_review_cycle_id'), 'reviews', ['review_cycle_id'], unique=False)

    # 6. Create other new tables (departments, teams, goals, competencies, feedback, ai foundations, relations)
    op.create_table('departments',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('head_id', sa.UUID(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['head_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teams',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('department_id', sa.UUID(), nullable=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('lead_id', sa.UUID(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
        sa.ForeignKeyConstraint(['lead_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('competencies',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    sa.Enum('NOT_STARTED', 'ON_TRACK', 'AT_RISK', 'BLOCKED', 'COMPLETED', name='goal_status').create(op.get_bind(), checkfirst=True)
    op.create_table('goals',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('employee_id', sa.UUID(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', postgresql.ENUM('NOT_STARTED', 'ON_TRACK', 'AT_RISK', 'BLOCKED', 'COMPLETED', name='goal_status', create_type=False), nullable=False),
        sa.Column('progress', sa.Integer(), nullable=False),
        sa.Column('due_date', sa.Date(), nullable=True),
        sa.Column('parent_goal_id', sa.UUID(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['employee_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
        sa.ForeignKeyConstraint(['parent_goal_id'], ['goals.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('review_templates',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    sa.Enum('PEER', 'MANAGER', 'SELF', 'GENERAL', name='feedback_type').create(op.get_bind(), checkfirst=True)
    op.create_table('feedback',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('author_id', sa.UUID(), nullable=False),
        sa.Column('recipient_id', sa.UUID(), nullable=False),
        sa.Column('review_cycle_id', sa.UUID(), nullable=True),
        sa.Column('feedback_type', postgresql.ENUM('PEER', 'MANAGER', 'SELF', 'GENERAL', name='feedback_type', create_type=False), nullable=False),
        sa.Column('project', sa.String(length=255), nullable=True),
        sa.Column('content_text', sa.Text(), nullable=False),
        sa.Column('tags', sa.String(length=255), nullable=True),
        sa.Column('is_requested', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
        sa.ForeignKeyConstraint(['recipient_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['review_cycle_id'], ['review_cycles.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ai_analysis',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('review_id', sa.UUID(), nullable=False),
        sa.Column('overall_score', sa.Integer(), nullable=True),
        sa.Column('confidence', sa.Float(), nullable=True),
        sa.Column('reasoning_summary', sa.Text(), nullable=True),
        sa.Column('raw_output', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['review_id'], ['reviews.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('evidence',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('review_id', sa.UUID(), nullable=False),
        sa.Column('source_type', sa.String(length=50), nullable=False),
        sa.Column('source_id', sa.UUID(), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['review_id'], ['reviews.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('review_competencies',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('review_id', sa.UUID(), nullable=False),
        sa.Column('competency_id', sa.UUID(), nullable=False),
        sa.Column('weight', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['competency_id'], ['competencies.id'], ),
        sa.ForeignKeyConstraint(['review_id'], ['reviews.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('review_goals',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('review_id', sa.UUID(), nullable=False),
        sa.Column('goal_id', sa.UUID(), nullable=False),
        sa.Column('weight', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['goal_id'], ['goals.id'], ),
        sa.ForeignKeyConstraint(['review_id'], ['reviews.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('review_participants',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('review_id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('participant_role', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['review_id'], ['reviews.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ai_insights',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('analysis_id', sa.UUID(), nullable=False),
        sa.Column('insight_type', sa.String(length=50), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['analysis_id'], ['ai_analysis.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ai_scores',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('analysis_id', sa.UUID(), nullable=False),
        sa.Column('dimension', sa.String(length=100), nullable=False),
        sa.Column('score', sa.Integer(), nullable=False),
        sa.Column('explanation', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['analysis_id'], ['ai_analysis.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bias_analysis',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('analysis_id', sa.UUID(), nullable=False),
        sa.Column('bias_type', sa.String(length=50), nullable=False),
        sa.Column('severity', sa.String(length=50), nullable=False),
        sa.Column('reason', sa.Text(), nullable=False),
        sa.Column('recommendation', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['analysis_id'], ['ai_analysis.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Adding columns to users, audit_events
    op.add_column('audit_events', sa.Column('organization_id', sa.UUID(), nullable=True))
    op.create_foreign_key(None, 'audit_events', 'organizations', ['organization_id'], ['id'])
    
    op.add_column('users', sa.Column('department_id', sa.UUID(), nullable=True))
    op.add_column('users', sa.Column('team_id', sa.UUID(), nullable=True))
    op.add_column('users', sa.Column('title', sa.String(length=255), nullable=True))
    op.create_foreign_key(None, 'users', 'teams', ['team_id'], ['id'])
    op.create_foreign_key(None, 'users', 'departments', ['department_id'], ['id'])
    
    # Need to update enums! (UserRole, ReviewStatus, etc)
    connection.execute(sa.text("ALTER TYPE user_role ADD VALUE IF NOT EXISTS 'SUPER_ADMIN'"))
    connection.execute(sa.text("ALTER TYPE user_role ADD VALUE IF NOT EXISTS 'ORG_ADMIN'"))
    connection.execute(sa.text("ALTER TYPE user_role ADD VALUE IF NOT EXISTS 'HR_ADMIN'"))
    connection.execute(sa.text("ALTER TYPE user_role ADD VALUE IF NOT EXISTS 'REVIEWER'"))
    
    # We rename 'review_cycle_status' to 'review_status' for the reviews table
    sa.Enum('DRAFT', 'IN_PROGRESS', 'AI_PROCESSING', 'MANAGER_REVIEW', 'PENDING_APPROVAL', 'APPROVED', 'EMPLOYEE_ACKNOWLEDGED', 'COMPLETED', name='review_status').create(op.get_bind(), checkfirst=True)
    connection.execute(sa.text("ALTER TABLE reviews ALTER COLUMN status DROP DEFAULT"))
    connection.execute(sa.text("ALTER TABLE reviews ALTER COLUMN status TYPE varchar(255)"))
    connection.execute(sa.text("UPDATE reviews SET status = 'IN_PROGRESS' WHERE status = 'ACTIVE'"))
    connection.execute(sa.text("UPDATE reviews SET status = 'AI_PROCESSING' WHERE status = 'PROCESSING'"))
    connection.execute(sa.text("ALTER TABLE reviews ALTER COLUMN status TYPE review_status USING status::review_status"))
    connection.execute(sa.text("ALTER TABLE reviews ALTER COLUMN status SET DEFAULT 'DRAFT'::review_status"))


def downgrade() -> None:
    pass
