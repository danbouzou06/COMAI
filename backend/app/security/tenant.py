from fastapi import Header, HTTPException, status


def require_organization(
    organization_id: str = Header(..., alias="X-Organization-Id"),
) -> str:
    if not organization_id.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Organisation invalide")
    return organization_id
