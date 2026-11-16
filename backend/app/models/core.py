from uuid import UUID

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDTimestampMixin


class Organization(UUIDTimestampMixin, Base):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(160))
    slug: Mapped[str] = mapped_column(String(160), unique=True, index=True)


class UserMembership(UUIDTimestampMixin, Base):
    __tablename__ = "user_memberships"

    user_id: Mapped[UUID] = mapped_column(index=True)
    organization_id: Mapped[UUID] = mapped_column(index=True)
    role: Mapped[str] = mapped_column(String(40), default="member")


class Client(UUIDTimestampMixin, Base):
    __tablename__ = "clients"

    organization_id: Mapped[UUID] = mapped_column(index=True)
    name: Mapped[str] = mapped_column(String(160))
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class Project(UUIDTimestampMixin, Base):
    __tablename__ = "projects"

    organization_id: Mapped[UUID] = mapped_column(index=True)
    client_id: Mapped[UUID | None] = mapped_column(nullable=True, index=True)
    name: Mapped[str] = mapped_column(String(160))
    status: Mapped[str] = mapped_column(String(40), default="active")
