import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, JSON, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDTimestampMixin


class Mission(UUIDTimestampMixin, Base):
    __tablename__ = "missions"

    organization_id: Mapped[uuid.UUID] = mapped_column(index=True)
    requested_by: Mapped[uuid.UUID] = mapped_column(index=True)
    project_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True, index=True)
    objective: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(40), default="pending", index=True)
    context: Mapped[dict] = mapped_column(JSON, default=dict)


class MissionTask(UUIDTimestampMixin, Base):
    __tablename__ = "mission_tasks"

    mission_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("missions.id", ondelete="CASCADE"), index=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(index=True)
    agent_id: Mapped[str] = mapped_column(String(80), index=True)
    status: Mapped[str] = mapped_column(String(40), default="pending", index=True)
    input_data: Mapped[dict] = mapped_column(JSON, default=dict)
    output_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)


class Deliverable(UUIDTimestampMixin, Base):
    __tablename__ = "deliverables"

    organization_id: Mapped[uuid.UUID] = mapped_column(index=True)
    mission_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("missions.id", ondelete="CASCADE"), index=True)
    kind: Mapped[str] = mapped_column(String(80))
    storage_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    content: Mapped[dict | None] = mapped_column(JSON, nullable=True)


class AuditEvent(UUIDTimestampMixin, Base):
    __tablename__ = "audit_events"

    organization_id: Mapped[uuid.UUID] = mapped_column(index=True)
    actor_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True, index=True)
    event_type: Mapped[str] = mapped_column(String(100), index=True)
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
