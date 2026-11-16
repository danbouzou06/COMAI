from typing import Literal

from pydantic import BaseModel, Field

TaskStatus = Literal[
    "pending",
    "running",
    "completed",
    "failed",
    "needs_review",
    "cancelled",
]


class AgentTask(BaseModel):
    task_id: str = Field(min_length=1)
    organization_id: str = Field(min_length=1)
    user_id: str = Field(min_length=1)
    client_id: str | None = None
    project_id: str | None = None
    objective: str = Field(min_length=1)
    instructions: str = ""
    context: dict[str, object] = Field(default_factory=dict)
    expected_output: str = ""
    constraints: list[str] = Field(default_factory=list)
    deadline: str | None = None
    authorized_tools: list[str] = Field(default_factory=list)


class AgentResult(BaseModel):
    agent_id: str
    task_id: str
    status: TaskStatus
    summary: str
    deliverables: list[dict[str, object]] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    estimated_usage: dict[str, float | int] = Field(default_factory=dict)
    next_recommendations: list[str] = Field(default_factory=list)


class AgentDescriptor(BaseModel):
    agent_id: str
    name: str
    description: str
    capabilities: list[str]
    authorized_tools: list[str]
