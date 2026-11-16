from fastapi import APIRouter

from app.agents.registry import registry
from app.schemas.agents import AgentDescriptor

router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("", response_model=list[AgentDescriptor])
def list_agents() -> list[AgentDescriptor]:
    return registry.list()
