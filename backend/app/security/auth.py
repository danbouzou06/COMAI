from typing import Any

from fastapi import Depends, Header, HTTPException, status
from jwt import InvalidTokenError, decode

from app.core.config import get_settings


def require_user(authorization: str = Header(...)) -> dict[str, Any]:
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bearer token requis")
    settings = get_settings()
    if not settings.supabase_jwt_secret:
        raise HTTPException(status_code=503, detail="Supabase Auth non configuré")
    try:
        return decode(token, settings.supabase_jwt_secret, algorithms=["HS256"], audience="authenticated")
    except InvalidTokenError as exc:
        raise HTTPException(status_code=401, detail="Jeton Supabase invalide") from exc


def require_user_organization(
    user: dict[str, Any] = Depends(require_user),
    organization_id: str = Header(..., alias="X-Organization-Id"),
) -> tuple[dict[str, Any], str]:
    allowed = user.get("app_metadata", {}).get("organization_ids", [])
    if organization_id not in allowed:
        raise HTTPException(status_code=403, detail="Accès refusé à cette organisation")
    return user, organization_id
