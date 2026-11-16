from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.core import Project
from app.models.missions import Mission


class OrganizationRepository:
    def __init__(self, session: AsyncSession, organization_id: UUID) -> None:
        self.session = session
        self.organization_id = organization_id

    async def list_projects(self) -> Sequence[Project]:
        result = await self.session.scalars(
            select(Project)
            .where(Project.organization_id == self.organization_id)
            .order_by(Project.created_at.desc())
        )
        return result.all()

    async def get_mission(self, mission_id: UUID) -> Mission | None:
        return await self.session.scalar(
            select(Mission).where(
                Mission.id == mission_id,
                Mission.organization_id == self.organization_id,
            )
        )

    async def add_mission(self, mission: Mission) -> Mission:
        if mission.organization_id != self.organization_id:
            raise ValueError("La mission appartient à une autre organisation")
        self.session.add(mission)
        await self.session.flush()
        return mission
