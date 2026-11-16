from uuid import UUID

from redis.asyncio import Redis

from app.core.config import get_settings


class MissionQueue:
    def __init__(self, redis: Redis | None = None) -> None:
        self.redis = redis or Redis.from_url(get_settings().redis_url, decode_responses=True)

    async def enqueue(self, organization_id: UUID, mission_id: UUID) -> None:
        await self.redis.rpush(
            "comai:missions",
            f"{organization_id}:{mission_id}",
        )

    async def close(self) -> None:
        await self.redis.aclose()
