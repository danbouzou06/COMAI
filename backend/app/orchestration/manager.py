from typing import Any
from uuid import UUID

from app.agents.registry import registry
from app.schemas.agents import AgentResult, AgentTask


class ComaiManager:
    def __init__(self, max_steps: int = 8) -> None:
        self.max_steps = max_steps

    def plan(self, task: AgentTask, agent_ids: list[str]) -> list[dict[str, Any]]:
        if not agent_ids:
            raise ValueError("Au moins un agent est requis")
        if len(agent_ids) > self.max_steps:
            raise ValueError("Le nombre maximal d'étapes est dépassé")
        for agent_id in agent_ids:
            registry.get(agent_id)
        return [{"agent_id": agent_id, "depends_on": []} for agent_id in agent_ids]

    async def execute_parallel(self, task: AgentTask, agent_ids: list[str]) -> list[AgentResult]:
        import asyncio

        self.plan(task, agent_ids)
        async def run(agent_id: str) -> AgentResult:
            return await registry.get(agent_id).execute(task)
        return list(await asyncio.gather(*(run(agent_id) for agent_id in agent_ids)))
