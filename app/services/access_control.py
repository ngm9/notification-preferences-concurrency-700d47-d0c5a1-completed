from uuid import UUID

from fastapi import HTTPException

from app.models.auth import TokenClaims


def authorize_preferences_access(
    claims: TokenClaims,
    target_user_id: UUID,
    target_tenant_id: UUID,
) -> None:
    if claims.tenant_id != target_tenant_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    if claims.user_id == target_user_id:
        return

    if claims.role == "admin":
        return

    raise HTTPException(status_code=403, detail="Forbidden")
