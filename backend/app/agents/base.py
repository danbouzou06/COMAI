from abc import ABC, abstractmethod

from app.schemas.agents import AgentDescriptor, AgentResult, AgentTask


class BaseAgent(ABC):
    descriptor: AgentDescriptor

    @abstractmethod
    async def execute(self, task: AgentTask) -> AgentResult:
        """Execute une mission et retourne un résultat structuré."""
        raise NotImplementedError
