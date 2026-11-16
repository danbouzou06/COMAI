"""initial COMAI schema

Revision ID: 0001_initial
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    uuid_type = postgresql.UUID(as_uuid=True)
    now = sa.text("now()")
    op.create_table("organizations", sa.Column("id", uuid_type, primary_key=True), sa.Column("name", sa.String(160), nullable=False), sa.Column("slug", sa.String(160), nullable=False, unique=True), sa.Column("created_at", sa.DateTime(timezone=True), server_default=now), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=now))
    op.create_table("user_memberships", sa.Column("id", uuid_type, primary_key=True), sa.Column("user_id", uuid_type, nullable=False), sa.Column("organization_id", uuid_type, nullable=False), sa.Column("role", sa.String(40), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=now), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=now))
    op.create_table("clients", sa.Column("id", uuid_type, primary_key=True), sa.Column("organization_id", uuid_type, nullable=False), sa.Column("name", sa.String(160), nullable=False), sa.Column("notes", sa.Text()), sa.Column("created_at", sa.DateTime(timezone=True), server_default=now), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=now))
    op.create_table("projects", sa.Column("id", uuid_type, primary_key=True), sa.Column("organization_id", uuid_type, nullable=False), sa.Column("client_id", uuid_type), sa.Column("name", sa.String(160), nullable=False), sa.Column("status", sa.String(40), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=now), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=now))
    op.create_table("missions", sa.Column("id", uuid_type, primary_key=True), sa.Column("organization_id", uuid_type, nullable=False), sa.Column("requested_by", uuid_type, nullable=False), sa.Column("project_id", uuid_type), sa.Column("objective", sa.Text(), nullable=False), sa.Column("status", sa.String(40), nullable=False), sa.Column("context", sa.JSON(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=now), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=now))
    op.create_table("mission_tasks", sa.Column("id", uuid_type, primary_key=True), sa.Column("mission_id", uuid_type, nullable=False), sa.Column("organization_id", uuid_type, nullable=False), sa.Column("agent_id", sa.String(80), nullable=False), sa.Column("status", sa.String(40), nullable=False), sa.Column("input_data", sa.JSON(), nullable=False), sa.Column("output_data", sa.JSON()), sa.Column("error_message", sa.Text()), sa.Column("created_at", sa.DateTime(timezone=True), server_default=now), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=now))
    op.create_table("deliverables", sa.Column("id", uuid_type, primary_key=True), sa.Column("organization_id", uuid_type, nullable=False), sa.Column("mission_id", uuid_type, nullable=False), sa.Column("kind", sa.String(80), nullable=False), sa.Column("storage_path", sa.String(500)), sa.Column("content", sa.JSON()), sa.Column("created_at", sa.DateTime(timezone=True), server_default=now), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=now))
    op.create_table("audit_events", sa.Column("id", uuid_type, primary_key=True), sa.Column("organization_id", uuid_type, nullable=False), sa.Column("actor_id", uuid_type), sa.Column("event_type", sa.String(100), nullable=False), sa.Column("payload", sa.JSON(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=now), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=now))


def downgrade() -> None:
    for table in ("audit_events", "deliverables", "mission_tasks", "missions", "projects", "clients", "user_memberships", "organizations"):
        op.drop_table(table)
