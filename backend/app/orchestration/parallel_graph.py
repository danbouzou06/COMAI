import asyncio
from typing import TypedDict

from langgraph.graph import END, StateGraph

from app.agents.registry import registry
from app.schemas.agents import AgentResult, AgentTask


class ParallelWorkflowState(TypedDict, total=False):
    task: AgentTask
    agent_ids: list[str]
    results: list[AgentResult]


async def run_parallel(state: ParallelWorkflowState) -> ParallelWorkflowState:
    async def execute(agent_id: str) -> AgentResult:
        return await registry.get(agent_id).execute(state["task"])

    results = await asyncio.gather(*(execute(agent_id) for agent_id in state["agent_ids"]))
    return {**state, "results": list(results)}


def build_parallel_graph():
    graph = StateGraph(ParallelWorkflowState)
    graph.add_node("run_parallel", run_parallel)
    graph.set_entry_point("run_parallel")
    graph.add_edge("run_parallel", END)
    return graph.compile()
