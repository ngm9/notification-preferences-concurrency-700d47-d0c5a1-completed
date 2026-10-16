from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.config import settings
from app.models.auth import TokenClaims

bearer_scheme = HTTPBearer()


def create_access_token(user_id: UUID, tenant_id: UUID, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=24)
    payload = {
        "user_id": str(user_id),
        "tenant_id": str(tenant_id),
        "role": role,
        "exp": expire,
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> TokenClaims:
    token = credentials.credentials

    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        return TokenClaims(
            user_id=payload["user_id"],
            tenant_id=payload["tenant_id"],
            role=payload["role"],
        )
    except (JWTError, KeyError):
        raise HTTPException(status_code=401, detail="Invalid or expired token")
