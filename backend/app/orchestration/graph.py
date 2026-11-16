from typing import TypedDict

from langgraph.graph import END, StateGraph

from app.agents.registry import registry
from app.schemas.agents import AgentResult, AgentTask


class WorkflowState(TypedDict, total=False):
    task: AgentTask
    results: list[AgentResult]


async def run_agent(state: WorkflowState) -> WorkflowState:
    task = state["task"]
    agent_id = task.context.get("agent_id", "strategist_ai")
    result = await registry.get(str(agent_id)).execute(task)
    return {"task": task, "results": [result]}


def build_single_agent_graph():
    graph = StateGraph(WorkflowState)
    graph.add_node("run_agent", run_agent)
    graph.set_entry_point("run_agent")
    graph.add_edge("run_agent", END)
    return graph.compile()
