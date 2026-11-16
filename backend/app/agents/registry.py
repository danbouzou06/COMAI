from app.agents.base import BaseAgent
from app.agents.specialists import CreativeAgent, CopywriterAgent, StrategistAgent
from app.schemas.agents import AgentDescriptor


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: dict[str, BaseAgent] = {}
        for agent in (StrategistAgent(), CopywriterAgent(), CreativeAgent()):
            self.register(agent)

    def register(self, agent: BaseAgent) -> None:
        agent_id = agent.descriptor.agent_id
        if agent_id in self._agents:
            raise ValueError(f"Agent déjà enregistré: {agent_id}")
        self._agents[agent_id] = agent

    def get(self, agent_id: str) -> BaseAgent:
        try:
            return self._agents[agent_id]
        except KeyError as exc:
            raise KeyError(f"Agent inconnu: {agent_id}") from exc

    def list(self) -> list[AgentDescriptor]:
        return [agent.descriptor for agent in self._agents.values()]


registry = AgentRegistry()
