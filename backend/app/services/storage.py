from pathlib import Path

from supabase import Client, create_client

from app.core.config import get_settings


class SupabaseStorage:
    def __init__(self, client: Client | None = None) -> None:
        settings = get_settings()
        if not settings.supabase_url or not settings.supabase_service_role_key:
            raise RuntimeError("SUPABASE_URL et SUPABASE_SERVICE_ROLE_KEY sont requis")
        self.client = client or create_client(settings.supabase_url, settings.supabase_service_role_key)
        self.bucket = settings.supabase_storage_bucket

    def upload(self, *, organization_id: str, filename: str, content: bytes, content_type: str) -> str:
        safe_name = Path(filename).name
        path = f"organizations/{organization_id}/{safe_name}"
        self.client.storage.from_(self.bucket).upload(
            path,
            content,
            {"content-type": content_type, "upsert": "false"},
        )
        return path

    def signed_url(self, path: str, expires_in: int = 3600) -> str:
        if not path.startswith("organizations/"):
            raise ValueError("Chemin Storage invalide")
        response = self.client.storage.from_(self.bucket).create_signed_url(path, expires_in)
        return response["signedURL"]
