from fastapi import APIRouter, HTTPException

from app.agents.registry import registry
from app.schemas.agents import AgentResult, AgentTask

router = APIRouter(prefix="/missions", tags=["missions"])


@router.post("/execute/{agent_id}", response_model=AgentResult)
async def execute_agent(agent_id: str, task: AgentTask) -> AgentResult:
    try:
        agent = registry.get(agent_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return await agent.execute(task)
