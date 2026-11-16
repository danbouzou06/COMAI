import asyncio
from uuid import UUID

from redis.asyncio import Redis

from app.agents.registry import registry
from app.core.config import get_settings
from app.schemas.agents import AgentTask


async def worker_loop() -> None:
    redis = Redis.from_url(get_settings().redis_url, decode_responses=True)
    try:
        while True:
            item = await redis.blpop("comai:missions", timeout=5)
            if not item:
                continue
            _, payload = item
            organization_id, mission_id = payload.split(":", maxsplit=1)
            # La lecture de la mission depuis PostgreSQL sera branchée ici.
            # Le périmètre organisationnel est conservé dans le message Redis.
            task = AgentTask(
                task_id=mission_id,
                organization_id=organization_id,
                user_id="worker",
                objective="Mission chargée depuis la file Redis",
            )
            await registry.get("strategist_ai").execute(task)
    finally:
        await redis.aclose()


if __name__ == "__main__":
    asyncio.run(worker_loop())
