from fastapi import APIRouter, Depends, HTTPException

from app.agents.registry import registry
from app.core.config import get_settings
from app.orchestration.manager import ComaiManager
from app.security.auth import require_user_organization
from app.schemas.agents import AgentResult, AgentTask

router = APIRouter(prefix="/missions", tags=["missions"])


@router.post("/execute/{agent_id}", response_model=AgentResult)
async def execute_agent(
    agent_id: str,
    task: AgentTask,
    identity=Depends(require_user_organization),
) -> AgentResult:
    if task.organization_id != identity[1]:
        raise HTTPException(status_code=403, detail="Organisation de la mission incohérente")
    try:
        agent = registry.get(agent_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return await agent.execute(task)


@router.post("/execute-parallel", response_model=list[AgentResult])
async def execute_parallel(
    task: AgentTask,
    agent_ids: list[str],
    identity=Depends(require_user_organization),
) -> list[AgentResult]:
    if task.organization_id != identity[1]:
        raise HTTPException(status_code=403, detail="Organisation de la mission incohérente")
    return await ComaiManager(get_settings().max_agent_steps).execute_parallel(task, agent_ids)
