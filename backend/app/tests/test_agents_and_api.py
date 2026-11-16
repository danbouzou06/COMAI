import pytest
from fastapi.testclient import TestClient

from app.agents.registry import registry
from app.main import app
from app.schemas.agents import AgentTask

client = TestClient(app)


@pytest.mark.parametrize("agent_id", ["strategist_ai", "copywriter_ai", "creative_ai"])
@pytest.mark.asyncio
async def test_registered_agents_return_structured_result(agent_id: str) -> None:
    task = AgentTask(
        task_id="task-1",
        organization_id="org-1",
        user_id="user-1",
        objective="Préparer une campagne à Niamey",
    )
    result = await registry.get(agent_id).execute(task)
    assert result.agent_id == agent_id
    assert result.task_id == "task-1"
    assert result.status == "needs_review"


def test_unknown_agent_is_rejected() -> None:
    with pytest.raises(KeyError):
        registry.get("unknown_agent")


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_agents_endpoint() -> None:
    response = client.get("/api/v1/agents")
    assert response.status_code == 200
    assert {item["agent_id"] for item in response.json()} == {
        "strategist_ai",
        "copywriter_ai",
        "creative_ai",
    }


def test_mission_endpoint() -> None:
    response = client.post(
        "/api/v1/missions/execute/strategist_ai",
        json={
            "task_id": "task-1",
            "organization_id": "org-1",
            "user_id": "user-1",
            "objective": "Préparer une campagne à Niamey",
        },
    )
    assert response.status_code == 200
    assert response.json()["agent_id"] == "strategist_ai"


def test_unknown_agent_endpoint() -> None:
    response = client.post(
        "/api/v1/missions/execute/unknown_agent",
        json={
            "task_id": "task-1",
            "organization_id": "org-1",
            "user_id": "user-1",
            "objective": "Mission test",
        },
    )
    assert response.status_code == 404
