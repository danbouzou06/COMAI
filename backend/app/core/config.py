from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "COMAI API"
    environment: str = "development"
    openai_api_key: str | None = None
    openai_text_model: str = "gpt-4o-mini"
    openai_image_model: str = "gpt-image-1"
    database_url: str = "postgresql+asyncpg://comai:comai@localhost:5432/comai"
    redis_url: str = "redis://localhost:6379/0"
    supabase_url: str | None = None
    supabase_jwt_secret: str | None = None
    supabase_service_role_key: str | None = None
    supabase_storage_bucket: str = "comai-deliverables"
    max_agent_steps: int = 8
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
